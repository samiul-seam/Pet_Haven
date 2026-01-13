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



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(pet_count=Count('pets')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


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
