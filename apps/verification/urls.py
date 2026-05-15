from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VerificationCheckViewSet, run_identity_api, run_address_api, trigger_field_api
router=DefaultRouter(); router.register('checks', VerificationCheckViewSet)
urlpatterns=router.urls+[path('identity/run/',run_identity_api),path('address/run/',run_address_api),path('field/trigger/',trigger_field_api)]
