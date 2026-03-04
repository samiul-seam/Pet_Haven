from django.http import HttpResponseRedirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from .models import Adopt, AdoptPet, Favorite
from .serializers import AdoptSerializer, FavoriteSerializer, UpdateAdoptSerializer
from .services import AdooptService
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from pets.models import Pet
from rest_framework import status
from rest_framework.decorators import api_view
from sslcommerz_lib import SSLCOMMERZ 
from django.conf import settings as main_settings
from rest_framework.views import APIView

class AdoptViewSet(ModelViewSet):
    serializer_class = AdoptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Adopt.objects.prefetch_related('adoptpets__pet').all()
        return Adopt.objects.prefetch_related('adoptpets__pet').filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        existing_adopt = Adopt.objects.filter(user=request.user).first()
        if existing_adopt:
            serializer = self.get_serializer(existing_adopt)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        pet = serializer.validated_data.pop('pet_id')

        if pet.is_adopted:
            raise ValidationError({"pet_id": f"Pet '{pet.name}' is already adopted."})
        
        already_requested = AdoptPet.objects.filter(pet=pet, adopt__user=self.request.user).exclude(adopt__status=Adopt.CANCELED).exists()

        if already_requested:
            raise ValidationError({"pet_id": "You have already Listed the pet for Adoption.Go and check the adoption list"})

        adopt = serializer.save(user=self.request.user)
        adopt.adoptpets.create(pet=pet)


    @action(detail=True, methods=['patch'], serializer_class=UpdateAdoptSerializer)
    def update_status(self, request, pk=None):
        adoption = self.get_object()
        serializer = UpdateAdoptSerializer(adoption, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f"Adoption status updated to {request.data['status']}"})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        adoption = self.get_object()
        AdooptService.cancel_adoption(adoption=adoption, user=request.user)
        return Response({'status': 'Adoption canceled'})

    @swagger_auto_schema(
        operation_summary="List Adoptions",
        operation_description="List all adoptions. Staff sees all, normal users see their own",
        responses={200: AdoptSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Adoption",
        operation_description="Retrieve details of a single adoption",
        responses={200: AdoptSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Adoption",
        operation_description="Create a new adoption for the authenticated user",
        request_body=AdoptSerializer,
        responses={201: AdoptSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Adoption",
        operation_description="Update an adoption (staff only)",
        request_body=AdoptSerializer,
        responses={200: AdoptSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        pet = serializer.validated_data["pet"]
        if Favorite.objects.filter(user=self.request.user,pet=pet).exists():
            raise ValidationError("You have already favorited this pet!")

        serializer.save(user=self.request.user)


@api_view(['POST'])
def initiate_payment(request):
    user = request.user
    amount = request.data.get("amount")
    adopt_id = request.data.get("AdoptId")

    settings = { 'store_id': 'petha69a4a68f4ef3b', 'store_pass': 'petha69a4a68f4ef3b@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"txn_{adopt_id}"
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/payment/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/payment/fail/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = "1"
    post_body['product_name'] = "E-commerce Pets"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body)  # API response

    if response.get("status") == 'SUCCESS':
        return Response({"payment_url": response['GatewayPageURL']})
    return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def payment_success(request):
    print("Inside success")
    adopt_id = request.data.get("tran_id").split('_')[1]

    adopt = Adopt.objects.get(id=adopt_id)
    adopt.status = "Paid"
    adopt.save()
    
    adoptpets=adopt.adoptpets.all()
    for adoptpet in adoptpets:
        pet= adoptpet.pet
        pet.is_adopted = True
        pet.save()
        
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/adoption/")


@api_view(['POST'])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/adoption/")


@api_view(['POST'])
def payment_fail(request):
    print("Inside fail")
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/adoption/")

class HasAdoptedPet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pet_id):
        user = request.user
        has_adopted = AdoptPet.objects.filter(adopt__user=user, pet_id=pet_id).exists()
        return Response({"hasAdopted": has_adopted})