from rest_framework import generics, permissions, renderers
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly

# creating an endpoint for the root of out API
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetHighlight(generics.GenericAPIView):
    # creating an endpoint for the highlighted snippets
    # we don't want to use JSON, but instead just present an HTML representation
    # there's no existing concrete generic view that we can use.
    # we're not returning an object instance, but instead a property of an object instance
    # so we'll use the base class for representing instances, and create our own get() method.
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class SnippetList(generics.ListCreateAPIView):
    # list all code snippets, or create a new snippet
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # associate snippets with users
    # the create() method of our serializer will now be passed an addtional 'owner' field,
    # along with the validated data from the request
    # request.user : Django User instance
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update, or delete a code snippet
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# create read-only views for the user representations
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
