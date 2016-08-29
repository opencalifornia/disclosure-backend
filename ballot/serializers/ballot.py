from rest_framework import serializers

from .office_election import OfficeElectionSerializer
from .referendum import ReferendumSerializer
from .. import models
from _django_utils import ExtendedModelSerializer


class BallotItemSerializer(serializers.ModelSerializer):
    contest_type = serializers.CharField(source='get_contest_type_display')

    def to_representation(self, obj):
        ballot_item = super(BallotItemSerializer, self).to_representation(obj)
        subclass_data = dict()
        if obj.contest_type == 'R':
            subclass_data = ReferendumSerializer(obj.referendum).data
        elif obj.contest_type == 'O':
            subclass_data = OfficeElectionSerializer(obj.officeelection).data

        subclass_data.update(ballot_item)
        return subclass_data

    class Meta:
        model = models.BallotItem
        exclude = ('ballot',)


class BallotSerializer(ExtendedModelSerializer):
    ballot_items = BallotItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Ballot
        rename = dict(locality='locality_id')
