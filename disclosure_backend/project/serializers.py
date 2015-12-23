from calaccess_raw.models.campaign import RcptCd
from rest_framework import serializers


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RcptCd
