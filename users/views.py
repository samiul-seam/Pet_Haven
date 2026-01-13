from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Wallet
from .serializers import WalletSerializer, WalletAdminSerializer

class WalletViewSet(viewsets.ModelViewSet):  # allow create/update
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class WalletAdminViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletAdminSerializer
    permission_classes = [IsAdminUser]
