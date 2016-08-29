from rest_framework import serializers

from .. import models
from _django_utils.serializers import ExtendedModelSerializer


class OfficeSerializer(serializers.ModelSerializer):
    locality_id = serializers.PrimaryKeyRelatedField(source='locality', read_only=True)

    class Meta:
        model = models.Office
        exclude = ('locality',)


class CandidateSerializer(ExtendedModelSerializer):
    party = serializers.CharField(max_length=50, source='party.name')
    ballot_item_id = serializers.PrimaryKeyRelatedField(source='ballot_item', read_only=True)
    office_election_id = serializers.PrimaryKeyRelatedField(
        source='office_election',
        read_only=True)

    class Meta:
        model = models.Candidate
        exclude = ('ballot_item', 'office_election')


class OfficeElectionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True)

    class Meta:
        model = models.OfficeElection
        exclude = ('ballot', 'contest_type', 'office')
        rename = dict(locality='locality_id', ballot_item='ballot_item_id')

    def to_representation(self, obj):
        office = OfficeSerializer(obj.office).data
        office_election = super(OfficeElectionSerializer, self).to_representation(obj)
        office.update(office_election)
        return office
