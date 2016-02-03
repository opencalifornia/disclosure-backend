from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from .models import IndependentMoney, Committee
from .serializers import IndependentMoneySerializer


class IndependentMoneyViewSet(viewsets.ViewSet):
    """
    A contribution is money that a filing committee has received.
    ---
    list:
      response_serializer: IndependentMoneySerializer:

    """
    renderer_classes = [JSONRenderer]
    queryset = IndependentMoney.objects.all()

    def list(self, request):
        """ List all contributions """
        obj = IndependentMoney.objects.all()[1:10]
        return Response(IndependentMoneySerializer(obj, many=True).data)


class CommitteeViewSet(viewsets.ViewSet):
    """
    A contribution is money that a filing committee has received.
    ---
    """
    renderer_classes = [JSONRenderer]
    queryset = Committee.objects.all()

    def retrieve(self, request, pk, format=None):
        """ Get a single contribution """
        return Response({
            'committee_id': 1234,
            'name': 'Americans for Liberty',
            'contribution_by_type': {
                'unitemized': 2916394,
                'self_funded': 512554,
                'political_party': 6426112,
                'individual': 11134547,
                'recipient_committee': 986229
            },
            'contribution_by_area': {
                'inside_location': 0.56,
                'inside_state': 0.38,
                'outside_state': 0.06
            }
        })

    @detail_route(['GET'])
    def contributors(self, request, pk):
        """
        Display summarized contributor information
        ---
        parameters:
          - name: locality_id
            description: The locality_id (can be city, county, state)
            paramType: path
            type: integer
            required: true
        """
        return Response([
            {
                'name': 'Samantha Brooks',
                'amount': 700,
                'date': '2015-04-12'
            },
            {
                'name': 'Lisa Sheppards',
                'amount': 700,
                'date': '2015-01-13'
            },
            {
                'name': 'Raoul Esponsito',
                'amount': 700,
                'date': '2015-04-04'
            }
        ])
