from django.urls import path
from .views import cxo, operations, compliance
urlpatterns=[path('cxo/',cxo),path('operations/',operations),path('compliance/',compliance)]
