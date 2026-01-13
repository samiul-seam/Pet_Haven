from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name
    

class Pet(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  related_name='pets')
    breed = models.CharField(max_length=50)
    age = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_adopted = models.BooleanField(default=False)

    class Availability(models.TextChoices):
        PUBLIC = 'Public'
        ANYONE = 'Anyone'

    availability = models.CharField(
        max_length=20,
        choices=Availability.choices,
        default=Availability.PUBLIC
    )

    class Meta:
        ordering = ['id',]

    def __str__(self):
        return self.name
    
class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')

class Review(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('pet', 'user')

    def __str__(self):
        return f"Review from {self.user.email} on {self.pet.name} at {self.created_at}"
