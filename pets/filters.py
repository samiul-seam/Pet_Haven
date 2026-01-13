from django_filters.rest_framework import FilterSet
from pets.models import Pet

class PetFilter(FilterSet):
    class Meta:
        model = Pet
        fields = {
            'category_id': ['exact'],
            'is_adopted': ['exact'],
        }
