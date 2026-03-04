from django.db import models
from uuid import uuid4
from users.models import User
from pets.models import Pet

class Adopt(models.Model):
    NOT_PAID = 'Not Paid'
    PAID = 'Paid'
    READY_TO_SHIP = 'Ready To Adopt'
    ADOPTED = 'Adopted'
    CANCELED = 'Canceled'

    STATUS_CHOICES = [
        (NOT_PAID, 'Pending'),
        (PAID, 'Paid'),
        (READY_TO_SHIP, 'Ready To Adopt'),
        (ADOPTED, 'Adopted'),
        (CANCELED, 'Canceled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoptions')

    name = models.CharField(max_length=100, default="Unknown")
    address = models.TextField(default="Unknown")
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_PAID)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} adoption {self.id}"


class AdoptPet(models.Model):
    adopt = models.ForeignKey(Adopt, on_delete=models.CASCADE, related_name='adoptpets')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['adopt', 'pet']


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'pet']