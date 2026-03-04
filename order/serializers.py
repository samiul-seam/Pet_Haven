from rest_framework import serializers
from .models import Adopt, AdoptPet, Favorite
from pets.models import Pet

class SimplePetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Pet
        fields = ['id', 'name', 'price', 'category_name', 'breed', 'is_adopted']
        read_only_fields = fields


class AdoptSerializer(serializers.ModelSerializer):
    pets = serializers.SerializerMethodField(read_only=True)

    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(),
        write_only=True
    )

    class Meta:
        model = Adopt
        fields = ['id', 'created_at', 'pets', 'status', 'name', 'address', 'phone_number', 'pet_id']
        read_only_fields = ['id', 'created_at', 'status', 'pets']
        
    def get_pets(self, obj):
        pets = [adopt_pet.pet for adopt_pet in obj.adoptpets.all()]
        return SimplePetSerializer(pets, many=True).data

    
class UpdateAdoptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopt
        fields = ['status']


class FavoriteSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer(read_only=True)
    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(),
        source="pet",
        write_only=True
    )

    class Meta:
        model = Favorite
        fields = ["id", "pet_id", "pet", "created_at"]
        read_only_fields = ["id", "created_at"]