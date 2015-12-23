from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def search_view(request):
    """
    Search for a location (or later, a person or ballot measure).
    NOTE: This endpoint is currently stubbed.
    ---
    parameters:
      - name: q
        description: The user's search query
        type: string
        paramType: query
    """
    return Response([{
        "name": "San Francisco",
        "type": "county",
        "fip_id": "6075"
    }])
