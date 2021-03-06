from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from . import serializers, permissions
from .models import UserProfile, ProfileFeedItem
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


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """return a hello message"""

        viewset = [
            'uses actions (list, create, retrieve, update, and partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message': 'Hello', 'viewset': viewset})

    def create(self, request):
        """Create a hello message"""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting object by its ID"""

        return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        """Updates entire object by its ID"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Partially updates object by its ID"""

        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """Deletes an object by its ID"""

        return Response({'http_method':'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles HTTP Protoccol for User Profile model"""

    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)


class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading, and updating profile feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""

        serializer.save(user_profile=self.request.user)
