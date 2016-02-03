from rest_framework import viewsets
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from ..serializers import BallotSerializer, ReferendumSerializer  # noqa
# from ..models import Ballot


class BallotViewSet(viewsets.ViewSet):
    """
    TODO: docstring
    ---
    ballot:
      response_serializer: BallotSerializer
    """
    renderer_classes = [JSONRenderer]

    @list_route(['GET'])
    def ballot(self, request, locality_id):
        return Response({
            'ballot_id': 'ballot1',
            'locality_id': str(locality_id),
            'contests': [
                {
                    'contest_type': 'office',
                    'name': 'Mayor'
                },
                {
                    'contest_type': 'office',
                    'name': 'City Auditor'
                },
                {
                    'contest_type': 'office',
                    'name': 'City Treasurer'
                },
                {
                    'contest_type': 'office',
                    'name': 'Distrit 1 City Council'
                },
                {
                    'contest_type': 'office',
                    'name': 'Distrit 3 City Council'
                },
                {
                    'contest_type': 'office',
                    'name': 'Distrit 5 City Council'
                },
                {
                    'contest_type': 'referendum',
                    'name': 'Measure AA'
                },
                {
                    'contest_type': 'referendum',
                    'name': 'Measure BB'
                },
                {
                    'contest_type': 'referendum',
                    'name': 'Measure CC'
                }
            ]
        })

    @detail_route(['GET'])
    def referendum(self, request, locality_id, referendum_id=None):
        """
        TODO: docstring
        ---
        """
        return Response({
            'measure_id': measure_id,
            'city': {
                'locality_id': locality_id,
                'location': {
                    'name': 'San Francisco'
                }
            },  # Not sure if city really makes sense here
            'number': 'BB',
            'full_text': 'Shall the Charter of the City of Oakland be amended '
                         'to provide the Public Ethics Commission greater '
                         'independence, broader enforcement authority, powers',
            'title': 'Ethics Commission Authority Increase Charter Amendment',
            'supporting_count': 4,
            'opposing_count': 6
        })
