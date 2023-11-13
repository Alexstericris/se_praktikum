from rest_framework import serializers

from .models import User, Log


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','email')

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Log
        fields=('id','recorded_time','action','initiator_id')