from rest_framework import serializers

from .. import models


class ReferendumSerializer(serializers.ModelSerializer):
    ballot_id = serializers.PrimaryKeyRelatedField(source='ballot.id', read_only=True)

    class Meta:
        model = models.Referendum
        exclude = ('ballot',)
