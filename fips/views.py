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
    query = request.query_params.get('q', '').lower()
    fips_data = [
        {"name": "San Francisco",
         "type": "county",
         "fip_id": "6075"},
        {"name": "Oakland",
         "type": "city",
         "fip_id": "1111"},
    ]
    return Response(filter(lambda v: query in v['name'].lower(),
                    fips_data))
