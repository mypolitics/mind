from mypolitics_mind.apps.sejm_members.models import Members

from mypolitics_mind.common.serializers import DynamicFieldsModelSerializer


class MemberSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'
