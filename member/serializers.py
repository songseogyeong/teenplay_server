from rest_framework import serializers

from member.models import Member, AdminAccount


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class AdminAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAccount
        fields = '__all__'
