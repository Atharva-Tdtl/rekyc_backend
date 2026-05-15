from rest_framework import serializers
from .models import RiskAssessment, WatchlistHit
class RiskAssessmentSerializer(serializers.ModelSerializer):
    class Meta: model=RiskAssessment; fields='__all__'
class WatchlistHitSerializer(serializers.ModelSerializer):
    class Meta: model=WatchlistHit; fields='__all__'
