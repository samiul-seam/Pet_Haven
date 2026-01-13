from .models import Category, Pet, PetImage, Review
from rest_framework import serializers
from pets.models import Pet
from order.models import AdoptPet

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetImage
        fields = ['id', 'image']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'pet_id', 'pet', 'user', 'rating', 'comment']
        read_only_fields = ['pet', 'user']

    def validate(self, attrs):
        pet_id = self.context['pet_id']
        user = self.context['user']

        if Review.objects.filter(pet_id=pet_id, user=user).exists():
            raise serializers.ValidationError("You have already reviewed this pet.")

        pet = Pet.objects.get(id=pet_id)
        if not pet.is_adopted:
            raise serializers.ValidationError("You can only review pets that are adopted.")

        adopted = AdoptPet.objects.filter(pet=pet, adopt__user=user).exists()
        if not adopted:
            raise serializers.ValidationError("You can only review pets you have adopted.")

        return attrs

    def create(self, validated_data):
        user = self.context['user']
        pet_id = self.context['pet_id']
        return Review.objects.create(user=user, pet_id=pet_id, **validated_data)


class SimpleReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment']


class PetSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True, read_only=True)
    reviews = SimpleReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'category', 'breed', 'age', 'price',
            'description', 'is_adopted', 'availability', 'images', 'reviews'
        ]

    def get_fields(self):
        fields = super().get_fields()
        user = self.context['request'].user

        if not user.is_staff:
            fields['is_adopted'].read_only = True 
            fields.pop('availability', None)

        return fields


class SimplePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'price']