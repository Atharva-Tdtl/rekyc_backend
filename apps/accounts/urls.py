from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, send_otp

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('send-otp/', send_otp),
    path('', include(router.urls)),
]
