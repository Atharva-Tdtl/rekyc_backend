from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RiskAssessmentViewSet, WatchlistHitViewSet, score_customer, fraud_customer
router=DefaultRouter(); router.register('assessments',RiskAssessmentViewSet); router.register('watchlist-hits',WatchlistHitViewSet)
urlpatterns=router.urls+[path('score/<int:customer_id>/',score_customer),path('fraud/<int:customer_id>/',fraud_customer)]
