from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Wallet
from .serializers import WalletSerializer, WalletAdminSerializer


class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return Wallet.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user': self.request.user}

    @swagger_auto_schema(
        operation_summary="List Wallets",
        operation_description="Get all wallets for the authenticated user",
        responses={200: WalletSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Wallet",
        operation_description="Create a new wallet for the authenticated user",
        request_body=WalletSerializer,
        responses={201: WalletSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Wallet",
        operation_description="Retrieve a specific wallet of the authenticated user",
        responses={200: WalletSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Wallet",
        operation_description="Update a wallet of the authenticated user",
        request_body=WalletSerializer,
        responses={200: WalletSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Wallet",
        operation_description="Delete a wallet of the authenticated user",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class WalletAdminViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletAdminSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Admin: List all Wallets",
        responses={200: WalletAdminSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Admin: Create Wallet And add User Wallet balance",
        request_body=WalletAdminSerializer,
        responses={201: WalletAdminSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
