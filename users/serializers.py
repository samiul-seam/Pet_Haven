from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer , UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import Wallet
from users.models import User
from order.serializers import AdoptSerializer


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance']


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'address']


class UserSerializer(BaseUserSerializer):
    wallet = serializers.DecimalField(
        source='wallet.balance', max_digits=10, decimal_places=2, read_only=True
    )
    adoption_history = AdoptSerializer(
        source='adoptions', many=True, read_only=True
    )

    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'phone_number', 'address', 'wallet', 'adoption_history'
        ]
        read_only_fields = ['adoption_history', 'wallet']
    

class WalletSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'email', 'balance']
        read_only_fields = ['email']

    def create(self, validated_data):
        user = self.context['user']
        amount = validated_data.get('balance', 0)

        wallet, created = Wallet.objects.get_or_create(user=user)

        wallet.balance += amount
        wallet.save()
        return wallet




class WalletAdminSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    email = serializers.CharField(source='user.email', read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Wallet
        fields = ['id', 'email', 'balance']

    def create(self, validated_data):
        user_id = validated_data['id']
        balance = validated_data['balance']

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        wallet = Wallet.objects.get_or_create(user=user)
        wallet.balance = balance
        wallet.save()
        return wallet
