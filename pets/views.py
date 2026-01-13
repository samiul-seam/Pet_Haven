from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from api.permissions import IsAdminOrReadAndPostOnly
from .permissions import IsReviewAuthorOrReadOnly
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.response import Response
from .models import Category, Pet, PetImage, Review
from .serializers import CategorySerializer, PetSerializer, PetImageSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import PetFilter
from drf_yasg.utils import swagger_auto_schema



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(pet_count=Count('pets')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Retrieve all categories",
        operation_description="Get a list of all categories with pet count",
        responses={200: CategorySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a single category",
        responses={200: CategorySerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new category",
        operation_description="Admin only",
        request_body=CategorySerializer,
        responses={201: CategorySerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a category",
        request_body=CategorySerializer,
        responses={200: CategorySerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a category",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PetViewSet(ModelViewSet):
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ['name', 'breed']
    filterset_class = PetFilter
    permission_classes = [IsAdminOrReadAndPostOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Pet.objects.prefetch_related('images').all()
        else:
            return Pet.objects.prefetch_related('images').filter(availability=Pet.Availability.PUBLIC).all()
        
    @swagger_auto_schema(
        operation_summary="Retrieve all pets",
        operation_description="Public users only see public pets",
        responses={200: PetSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a single pet",
        responses={200: PetSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new pet",
        operation_description="User can create pet but cannot edit or delete",
        request_body=PetSerializer,
        responses={201: PetSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a pet",
        operation_description="Admin only",
        request_body=PetSerializer,
        responses={200: PetSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a pet",
        operation_description="Admin only",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method="post",
        operation_summary="Mark pet as adopted",
        operation_description="Admin only",
        responses={200: "Pet marked as adopted"}
    )


    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def adopt(self, request, pk=None):
        pet = self.get_object()
        pet.is_adopted = True
        pet.save()
        return Response({'status': 'Pet marked as adopted'})


class PetImageViewSet(ModelViewSet):
    serializer_class = PetImageSerializer
    permission_classes = [IsAdminOrReadAndPostOnly]

    def get_queryset(self):
        return PetImage.objects.filter(pet_id=self.kwargs.get('pet_pk'))

    def perform_create(self, serializer):
        serializer.save(pet_id=self.kwargs.get('pet_pk'))

    @swagger_auto_schema(
        operation_summary="Retrieve all images for a pet",
        responses={200: PetImageSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Add image to a pet",
        request_body=PetImageSerializer,
        responses={201: PetImageSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(pet_id=self.kwargs.get('pet_pk'))

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_context(self):
        return {
            'pet_id': self.kwargs.get('pet_pk'),
            'user': self.request.user,  
        }

    @swagger_auto_schema(
        operation_summary="Retrieve all reviews for a pet",
        responses={200: ReviewSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a single review",
        responses={200: ReviewSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a review",
        operation_description="Only users who adopted the pet can review",
        request_body=ReviewSerializer,
        responses={201: ReviewSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a review",
        request_body=ReviewSerializer,
        responses={200: ReviewSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a review",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)