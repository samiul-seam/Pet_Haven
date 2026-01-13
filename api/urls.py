from django.urls import path, include
from rest_framework_nested import routers
from pets.views import PetViewSet, CategoryViewSet, PetImageViewSet, ReviewViewSet
from order.views import AdoptViewSet, AdoptPetViewSet
from users.views import WalletViewSet, WalletAdminViewSet
# from order.views import AdoptViewSet


router = routers.DefaultRouter()
router.register('pets', PetViewSet, basename='pets')
router.register('categories', CategoryViewSet)
router.register('adoptions', AdoptViewSet, basename='adoptions')
router.register('wallet', WalletViewSet, basename='wallet')          
router.register('admin/wallet', WalletAdminViewSet, basename='admin-wallet') 


pet_router = routers.NestedDefaultRouter(
    router, 'pets', lookup='pet')
pet_router.register('reviews', ReviewViewSet, basename='pet-reviews')
pet_router.register('images', PetImageViewSet, basename='pet-images')

adopt_router = routers.NestedDefaultRouter(
    router, 'adoptions', lookup='adopt')
adopt_router.register('pets', AdoptPetViewSet, basename='adopt-pet')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(pet_router.urls)),
    path('', include(adopt_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
]