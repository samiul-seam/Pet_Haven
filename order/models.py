from django.db import models
from uuid import uuid4
from users.models import User
from pets.models import Pet

class Adopt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoptions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} adoption {self.id}"


class AdoptPet(models.Model):
    adopt = models.ForeignKey(Adopt, on_delete=models.CASCADE, related_name='adoptpets')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pet.name} in adoption {self.adopt.id}"
