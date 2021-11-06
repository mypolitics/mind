from apps.sejm_members.models import Members

from common.serializers import DynamicFieldsModelSerializer


class MemberSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'
