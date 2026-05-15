from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaseViewSet, TraceViewSet

router = DefaultRouter()
router.register(r'list', CaseViewSet, basename='case')
router.register(r'traces', TraceViewSet, basename='trace')

urlpatterns = [
    path('', include(router.urls)),
]
