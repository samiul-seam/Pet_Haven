from django.urls import path, include
from rest_framework_nested import routers
from pets.views import PetViewSet, CategoryViewSet, PetImageViewSet, ReviewViewSet
from order.views import AdoptViewSet, FavoriteViewSet, initiate_payment, payment_success, payment_fail, payment_cancel, HasAdoptedPet



router = routers.DefaultRouter()
router.register('pets', PetViewSet, basename='pets')
router.register('categories', CategoryViewSet)
router.register('adoptions', AdoptViewSet, basename='adoptions')
router.register('favorites', FavoriteViewSet, basename='favorites')

pet_router = routers.NestedDefaultRouter(
    router, 'pets', lookup='pet')
pet_router.register('reviews', ReviewViewSet, basename='pet-reviews')
pet_router.register('images', PetImageViewSet, basename='pet-images')



urlpatterns = [
    path('', include(router.urls)),
    path('', include(pet_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    path("payment/initiate/", initiate_payment, name="initiate-payment"),
    path("payment/success/", payment_success, name="payment-success"),
    path("payment/fail/", payment_fail, name="payment-fail"),
    path("payment/cancel/", payment_cancel, name="payment-cancel"),
    path("adoptions/has-adopted/<int:pet_id>/", HasAdoptedPet.as_view()),
]