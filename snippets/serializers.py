from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Snippet


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    # now that snippets are associated with the user that created them,
    # add the serializer field to reflect that
    # source : controls which attribute is used to populate a field, and can point at any attribute on the serialized instance
    # CharField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']
