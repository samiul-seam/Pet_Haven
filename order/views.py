from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Adopt, AdoptPet
from .serializers import AdoptSerializer, AdoptPetSerializer

class AdoptViewSet(ModelViewSet):
    serializer_class = AdoptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Adopt.objects.prefetch_related('adoptpets__pet').all()
        return Adopt.objects.prefetch_related('adoptpets__pet').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdoptPetViewSet(ModelViewSet):
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        adopt_id = self.kwargs['adopt_pk']
        return AdoptPet.objects.filter(adopt_id=adopt_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdoptPetSerializer
        return AdoptPetSerializer 
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['adopt_id'] = self.kwargs['adopt_pk']
        return context
