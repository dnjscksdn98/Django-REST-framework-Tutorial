from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Snippet


class SnippetSerializer(serializers.ModelSerializer):
    # now that snippets are associated with the user that created them,
    # add the serializer field to reflect that
    # source : controls which attribute is used to populate a field, and can point at any attribute on the serialized instance
    # CharField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos',
                  'language', 'style', 'owner']


class UserSerializer(serializers.ModelSerializer):
    # snippets is a reverse relationship on the User model,
    # it will not be included by default when using the ModelSerializer class,
    # so we needed to add an explicit field for it
    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']
