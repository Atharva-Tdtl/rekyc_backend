from rest_framework.routers import DefaultRouter
from .views import KYCDocumentViewSet
router=DefaultRouter(); router.register('', KYCDocumentViewSet)
urlpatterns=router.urls
