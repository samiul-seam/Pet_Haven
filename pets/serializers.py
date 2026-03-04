from .models import Category, Pet, PetImage, Review
from rest_framework import serializers
from pets.models import Pet
from order.models import AdoptPet

class CategorySerializer(serializers.ModelSerializer):
    num_pets = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'num_pets']


class PetImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = PetImage
        fields = ['id', 'image']


class SimpleReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment']


class PetSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True, read_only=True)
    reviews = SimpleReviewSerializer(many=True, read_only=True)
    category_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'category', 'category_name', 'breed', 'age', 'price', 'description', 'is_adopted',  'images', 'reviews'
        ]
        # read_only_fields = ['is_adopted']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else "No Category"

    def get_fields(self):
        fields = super().get_fields()
        # user = self.context['request'].user
        request = self.context.get('request')

        if not request:
            return fields     # Get problem by swagger , so have to change like this.
        user = request.user
        
        if not user.is_staff:
            fields['is_adopted'].read_only = True 
            
        return fields


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'pet_id', 'user', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = [ 'user']

    def validate(self, attrs):
        pet_id = self.context['pet_id']
        user = self.context['user']

        existing_review = Review.objects.filter(pet_id=pet_id, user=user)

        if self.instance is None:
            if existing_review.exists():
                raise serializers.ValidationError("You have already reviewed this pet.")

        else:
            if existing_review.exclude(id=self.instance.id).exists():
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



class SimplePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'price']