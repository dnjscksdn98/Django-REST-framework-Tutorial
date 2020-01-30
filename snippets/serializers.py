from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Snippet


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    # now that snippets are associated with the user that created them,
    # add the serializer field to reflect that
    # ReadOnlyField : when including field names that relate to an attribute rather than a model field.
    # source : controls which attribute is used to populate a field, and can point at any attribute on the serialized instance
    # CharField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    # The url field will be represented using a HyperlinkedIdentityField serializer field
    # There needs to be a way of determining which views should be used for hyperlinking to model instances.
    # You can override a URL field view name and lookup field by using either, or both of, the view_name and lookup_field options
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight',
        format='html'
    )

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # any relationships on the model will be represented using a HyperlinkedRelatedField serializer field.
    snippets = serializers.HyperlinkedRelatedField(
        view_name='snippet-detail',
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']
