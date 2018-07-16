from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers

# Create your views here.

class HelloApiView(APIView):
    """Test API View"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list"""

        view = [
            'Uses HTTP methods',
            'similar to a traditional django view',
            'Gives you most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'api_view':view})

    def post(self, request):
        """Create a new object and return it"""

        serializer = serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}!'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk=None):
        """Updates the entire model"""

        return Response({'method':'PUT'})

    def patch(self, request, pk=None):
        """Updates only specified fields of model"""

        return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
        """Deletes a model"""

        return Response({'method': 'DELETE'})
