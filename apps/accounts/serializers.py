from django.contrib.auth.models import User, Group
from rest_framework import serializers
class UserSerializer(serializers.ModelSerializer):
    groups=serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    class Meta: model=User; fields=['id','username','first_name','last_name','email','is_active','groups']
