from rest_framework import serializers
from .models import Adopt, AdoptPet
from pets.models import Pet
from pets.serializers import PetSerializer

class SimplePetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Pet
        fields = ['name', 'category_name', 'breed']
        read_only_fields = fields


class AdoptPetSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer(read_only=True)
    pet_id = serializers.IntegerField(write_only=True)


    class Meta:
        model = AdoptPet
        fields = ['id', 'pet_id', 'pet']

    def validate_pet_id(self, value):
        try:
            pet = Pet.objects.get(pk=value)
        except Pet.DoesNotExist:
            raise serializers.ValidationError("Pet does not exist")
        if pet.is_adopted:
            raise serializers.ValidationError(f"Pet '{pet.name}' is already adopted")
        user = self.context['request'].user
        if user.wallet.balance < pet.price:
            raise serializers.ValidationError("Insufficient wallet balance")
        return value

    def create(self, validated_data):
        adopt_id = self.context['adopt_id']
        pet_id = validated_data['pet_id']
        pet = Pet.objects.get(pk=pet_id)
        user = self.context['request'].user

        user.wallet.balance -= pet.price
        user.wallet.save()
        pet.is_adopted = True
        pet.save()

        adopt_pet = AdoptPet.objects.create(adopt_id=adopt_id, pet=pet)
        return adopt_pet


class AdoptSerializer(serializers.ModelSerializer):
    adoptpets = AdoptPetSerializer(many=True, read_only=True)
    user_balance = serializers.DecimalField(source='user.wallet.balance', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Adopt
        fields = ['id','created_at', 'user_balance', 'adoptpets']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        user = self.context['request'].user

        if Adopt.objects.filter(user=user).exists():
            raise serializers.ValidationError("You already have an active adoption.")

        return attrs