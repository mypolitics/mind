from apps.sejm_votings.models import Voting
from rest_framework import serializers
from common.serializers import DynamicFieldsModelSerializer


class VotingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Voting
        fields = '__all__'


class CompareSerializer(serializers.Serializer):
    party_1 = serializers.CharField()
    party_2 = serializers.CharField()
    value = serializers.FloatField()
