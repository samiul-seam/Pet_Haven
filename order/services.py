from .models import Adopt, Favorite
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


class AdooptService:
    @staticmethod
    def cancel_adoption(adoption, user):
        if user.is_staff:
            adoption.status= Adopt.CANCELED
            adoption.save()
            return adoption
        
        if adoption.user != user:
            raise PermissionDenied({'detail': "You can only cancel your own adoption."})
        
        if adoption.status != Adopt.NOT_PAID:
            raise ValidationError({'detail': "You can only cancel before payment."})

        adoption.status = Adopt.CANCELED
        adoption.save()
        return adoption
