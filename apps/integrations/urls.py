from django.urls import path
from .views import health, ckyc_fetch
urlpatterns=[path('health/',health), path('ckyc/<int:customer_id>/',ckyc_fetch)]
