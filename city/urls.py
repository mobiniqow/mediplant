from django.urls import path, include
from rest_framework import routers
from .views import CountryViewSet, CityViewSet

router = routers.DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'cities', CityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
