from django.contrib.auth.models import User
from rest_framework import serializers
from .models import SensorValue, WaterPumpeLogs

class SensorValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorValue
        fields = [
            'id',
            'air_temp',
            'pressure',
            'air_hum',
            'soil_hum',
            'soil_temp',
            'light',
            'timestamp',
            'status',
        ]

class CriticaValuesSerializer(serializers.Serializer):
    air_temp_min = serializers.FloatField()
    air_temp_max = serializers.FloatField()
    air_hum_min = serializers.FloatField()
    air_hum_max = serializers.FloatField()
    soil_temp_min = serializers.FloatField()
    soil_temp_max = serializers.FloatField()
    soil_hum_min = serializers.FloatField()
    soil_hum_max = serializers.FloatField()
    light_min = serializers.FloatField()
    light_max = serializers.FloatField()
    pressure_min = serializers.FloatField()
    pressure_max = serializers.FloatField()


class WaterPumpeLogsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = WaterPumpeLogs
        fields = [
            'id',
            'start',
            'end',
            'user',
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

