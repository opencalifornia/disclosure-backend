from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FipsEntity
from .serializers import FipsSerializer


@api_view(['GET'])
def search_view(request):
    """
    Search for a location.
    ---
    parameters:
      - name: q
        description: The user's search query
        type: string
        paramType: query
    """
    query = request.query_params.get('q', '').lower()
    query_set = FipsEntity.objects.filter(name__icontains=query)
    serializer = FipsSerializer(query_set, many=True)
    return Response(serializer.data)
