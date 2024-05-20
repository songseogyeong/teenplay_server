from rest_framework import serializers
from teenplay.models import TeenPlay


class TeenplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeenPlay
        fields = '__all__'