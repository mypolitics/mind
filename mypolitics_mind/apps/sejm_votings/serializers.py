from mypolitics_mind.apps.sejm_votings.models import Voting

from mypolitics_mind.common.serializers import DynamicFieldsModelSerializer


class VotingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Voting
        fields = '__all__'
