from mypolitics_mind.apps.news.models import News
from mypolitics_mind.common.serializers import DynamicFieldsModelSerializer


class NewsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
