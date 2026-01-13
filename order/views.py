from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Adopt, AdoptPet
from .serializers import AdoptSerializer, AdoptPetSerializer

class AdoptViewSet(ModelViewSet):
    serializer_class = AdoptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        if self.request.user.is_staff:
            return Adopt.objects.prefetch_related('adoptpets__pet').all()
        return Adopt.objects.prefetch_related('adoptpets__pet').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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


class AdoptPetViewSet(ModelViewSet):
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        adopt_id = self.kwargs['adopt_pk']
        return AdoptPet.objects.filter(adopt_id=adopt_id)

    def get_serializer_class(self):
        return AdoptPetSerializer

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        context = super().get_serializer_context()
        context['adopt_id'] = self.kwargs['adopt_pk']
        return context

    @swagger_auto_schema(
        operation_summary="List Adopted Pets",
        operation_description="List all pets in a specific adoption",
        responses={200: AdoptPetSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Add Pet to Adoption",
        operation_description="Add a new pet to a specific adoption",
        request_body=AdoptPetSerializer,
        responses={201: AdoptPetSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
