from django.contrib import admin
from .models import Adopt, AdoptPet


class AdoptPetInline(admin.TabularInline):
    model = AdoptPet
    extra = 1


@admin.register(Adopt)
class AdoptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'id')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at')
    inlines = [AdoptPetInline]


@admin.register(AdoptPet)
class AdoptPetAdmin(admin.ModelAdmin):
    list_display = ('id', 'adopt', 'pet')
    search_fields = ('adopt__id', 'pet__name')
