from calaccess_raw.models.campaign import RcptCd
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .serializers import ContributionSerializer


class Contribution(viewsets.ViewSet):
    """
    A contribution is money that an filing committee has received.
    ---
    retrieve:
      response_serializer: ContributionSerializer
    list:
      response_serializer: ContributionSerializer
    """
    renderer_classes = [JSONRenderer]
    queryset = RcptCd.objects.all()

    def list(self, request):
        """ List all contributions """
        obj = RcptCd.objects.all()[1:10]
        return Response(ContributionSerializer(obj, many=True).data)

    def retrieve(self, request, pk=None, format=None):
        """ Get a single contribution """
        obj = RcptCd.objects.get(id=pk)
        return Response(ContributionSerializer(obj).data)


@api_view(['GET'])
def location_view(request, fips_id):
    """
    Display summarized information about a location
    NOTE: This is stubbed to always return the same thing.
    ---
    parameters:
      - name: fips_id
        description: The Federal Information Processing Standards (FIPS) code for this locality.
        paramType: path
        type: integer
        required: true
    response_serializer: LocationSerializer
    """
    return Response({
        "location": {
            "name": "San Francisco",
            "fip_id": "1234",
            "next_election": "2015-11-04"
        },
        "contribution_total": 21425389,
        "contribution_by_type": {
            "individual": 11134547,
            "political_party": 6426112,
            "unitemized": 2916394,
            "recipient_committee": 986229,
            "self_funded": 512554
        },
        "contribution_by_area": {
            "inside_location": 0.56,
            "inside_state": 0.38,
            "outside_state": 0.06
        }
    }, content_type='application/json')


def homepage_view(request):
    return HttpResponse("""
        <a href='/docs/'>Check out the API Documentation</a>
        <br/>
        <a href='/admin/'>View the admin interface / database data.</a>
    """)
