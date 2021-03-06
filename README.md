# Django REST framework tutorial

## Setting up a new environment

<pre>
<code>
python -m venv env
source env/Scripts/activate

pip install django djangorestframework
</code>
</pre>

## Getting started

<pre>
<code>
django-admin startproject tutorial
cd tutorial

python manage.py startapp snippets
</code>
</pre>

## Create migration

<pre>
<code>
python manage.py makemigrations snippets
python manage.py migrate
</code>
</pre>

## Creating a Serializer class

[Serializer][document-link]

[document-link]: https://www.django-rest-framework.org/api-guide/serializers/#serializers

The first thing we need to get started on our Web API is to provide a way of serializing and deserializing the snippet instances
into representations such as _json_. We can do this by declaring serializers that work very similar to Django's forms.

## Using ModelSerializers

Our SnippetSerializer class is replicating a lot of information that's also contained in the Snippet model.
It would be nice if we could keep our code a bit more concise.

In the same way that Django provides both _Form_ classes and _ModelForm_ classes,
REST framework includes both _Serializer_ classes and _ModelSerializer_ classes.

They don't do anything particularly magical, they are simply a shortcut for creating serializer classes.

- An automatically determined set of fields
- Simple default implementations for the _create()_ and _update()_ methods

## Serializer fields

### Core arguments

**- source**

The name of the attribute that will be used to populate the field.

### ReadOnlyField

A field class that simply returns the value of the field without modification.
This field is used by default with ModelSerializer when including field names that relate to an attribute rather than a model field.

## Request objects

_Request_ object extends the regular _HttpRequest_, and provides more flexible request parsing.
The core funcionality of the _Request_ object is the _request.data_ attribute,
which is similar to _request.POST_, but more useful for working with Web APIs.

<pre>
<code>
request.POST // Only handles form data. Only works for 'POST' method.
request.data // Handles arbitrary data. Works for 'POST', 'PUT', and 'PATCH' method.
</code>
</pre>

## Response objects

REST framework supports HTTP content negotiation by providing a _Response_ class
which allows you to return content that can be rendered into multiple content types, depending on the client request.

_Response_ objects are initialised with data, which should consist of native Python primitives.
REST framework then uses standard HTTP content negotiation to determine how it should render the final response content.

 <pre>
 <code>
 return Response(data) // Renders to content type as requested by the client
 </code>
 </pre>

## Status codes

REST framework provides more explicit identifiers for each status code,
such ad _HTTP_400_BAD_REQUEST_ in the status module.
It's a good idea to use these throughout rather than using numeric identifiers.

## Wrapping API views

1. The _@api_view_ decorator for working with _function based_ views.
2. the _APIView_ class for working with _class based_ views.

These wrappers provide a fer bits of functionality such as making sure you receive _Request_ instances in your view,
and adding context to _Response_ objects so that content negotiation can be performed.

## Format suffixes

Using format suffixes gives us URLs that explicity refer to a given format.
Add _format_ keyword argument.

If responses are no longer hardwired to a single content type add _format=None_.

Now update urls file, to appent a set of _format_suffix_patterns_ in addition to the existing URLs.

<pre>
<code>
from rest_framework.urlpatterns import format_suffix_patterns

// urlpatterns = [...]

urlpatterns = format_suffix_patterns(urlpatterns)
</code>
</pre>

## Clase-based Views

<pre>
<code>
from rest_framework.decorators import APIView

class SnippetList(APIView):
</code>
</pre>

## Generic Views

REST framework takes advantage by providing a number of pre-built views that provide for commonly used patterns.
The generic views provided by REST framework allow you to quickly build API views that map closely to your database models.

If the generic views don't suit the needs of your API, you can drop down to using the regular _APIView_ class,
or reuse the mixins and base classes used by the generic views to compose your own set of reusable generic views.

### GenericAPIView

This class extends REST framework's _APIView_ class, adding commonly required behavior for standard list and detail views.
Each of the concrete generic views provided is built by combining _GenericAPIView_, with one or more mixin classes.

#### Attributes

**- queryset**

The queryset that should be used for returning objects from this view.

**- serializer_class**

The serializer class that should be used for validating and deserializing input, and for serializing output.

**- lookup_field**

The model field that should be used to for performing object lookup of individual model instances.
Defaults to _'pk'_.

#### Method

##### Save and deletion hooks

The following methods are provided by the mixin classes, and provide easy overriding of the object save or deletion behavior.

**- perform_create(self, serializer)**

Called by CreateModelMixin when saving a new object instance.

**- perform_update(self, serializer)**

Called by UpdateModelMixin when saving an existing object instance.

**- perform_destroy(self, serializer)**

Called by DestroyModelMixin when deleting an object instance.

These hooks are particularly useful for setting attributes that are implicit in the request, but are not part of the request data.
For instance, you might set an attribute on the object based on the request user, or based on a URL keyword argument.

<pre>
<code>
def perform_create(self, serializer):
    serializer.save(user=self.request.user)
</code>
</pre>

## Mixins

One of the big wins of using class-based views is that it allows us to easily compose reusable bits of behaviour.

The create/retreive/update/delete operations that we've been using so far are going to be pretty similar for any
model-backed API views we create.
Those bits of common behaviour are implemented in REST framework's mixin classes.

### ListModelMixin

Provides a _list(request, \*args, \*\*kwargs)_ method, that implements listing a queryset.
If the queryset is populated, this returns a _200 OK_ response, with a serialized representation of the queryset as the body of the response.

### CreateModelMixin

Provides a _create(request, \*args, \*\*kwargs)_ method, that implements creating and saving a new model instance.
If an object is created this returns a _201 Created_ response, with a serialized representation of the object as the body of the response.
If the request data provided for creating the object was invalid, a _400 Bad Request_ response will be returned, with the error details as the body of the response.

### RetrieveModelMixin

Provides a _retrieve(request, \*args, \*\*kwargs)_ method, that implements returning an existing model instance in a response.
If an object can be retrieved this returns a _200 OK_ response, with a serialized representation of the object as the body of the response.
Otherwise it will return a _404 Not Found_.

### UpdateModelMixin

Provides a _update(request, \*args, \*\*kwargs)_ method, that implements updating and saving an existing model instance.
If an object is updated this returns a _200 OK_ response, with a serialized representation of the object as the body of the response.
If the request data provided for updating the object was invalid, a _400 Bad Request_ response will be returned,
with the error details as the body of the response.

### DestroyModelMixin

Provides a _destroy(request, \*args, \*\*kwargs)_ method, that implements deletion of an existing model instance.
If an object is deleted this returns a _204 No Content_ response, otherwise it will return a _404 Not Found_.

## Concrete View Classes

REST framework provides a set of already mixed-in generic views that we can use to trim down our _views.py_ module even more.

### CreateAPIView

Used for create-only endpoints.
Provides a _post_ method handler.

### ListAPIView

Used for read-only endpoints to represent a collection of model instances.
Provides a _get_ method handler.

### RetrieveAPIView

Used for read-only endpoints to represent a single model instance.
Provides a _get_ method handler.

### DestroyAPIView

Used for update-only endpoints for a single model instance.
Provides _put_ and _patch_ method handlers.

### UpdateAPIView

Used for update-only endpoints for a single model instance.
Provides _put_ and _patch_ method handlers.

### ListCreateAPIView

Used for read-write endpoints to represent a collection of model instances.
Provides _get_ and _post_ method handlers.

### RetrieveUpdateAPIView

Used for read or update endpoints to represent a single model instance.
Provides _get_, _put_ and _patch_ method handlers.

### RetrieveDestroyAPIView

Used for read or delete endpoints to represent a single model instance.
Provides _get_ and _delete_ method handlers.

### RetrieveUpdateDestroyAPIView

Used for read-write-delete endpoints to represent a single model instance.
Provides _get_, _put_, _patch_ and _delete_ method handlers.

## Permissions

### Setting the permission policy

The default permission policy may be set globally, using the _DEFAULT_PERMISSION_CLASSES_ setting.

<pre>
<code>
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
</code>
</pre>

You can also set the authentication policy on a per-view, or per-viewset basis, using the APIView class-based views.

<pre>
<code>
from rest_framework.permissions import IsAuthenticated

class ExampleView(APIView):
    permission_classes = [IsAuthenticated]
</code>
</pre>

Or, if you're using the @api_view decorator with function based views.

<pre>
<code>
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    //
</code>
</pre>

### API Reference

**- AllowAny**

The _AllowAny_ permission class will allow unrestricted access,
regardless of if the request was authenticated or unauthenticated.

**- IsAuthenticated**

The _IsAuthenticated_ permission class will deny permission to any unauthenticated user,
and allow permission otherwise.

**- IsAdminUser**

The _IsAdminUser_ permission class will deny permission to any user,
unless _user.is_staff_ is _True_ in which case permission will be allowed.'

**- IsAuthenticatedOrReadOnly**

The _IsAuthenticatedOrReadOnly_ will allow authenticated users to perform any request.
Requests for unauthorised users will only be permitted if the request method is one of the "safe" methods; _GET_, _HEAD_ or _OPTIONS_.

This permission is suitable if you want your API to allow read permissions to anonymous users,
and only allow write permissions to authenticated users.

## Authentications

Authentication always run at the very start of the view,
before the permission and throttling checks occur,
and before any other code is allowed to proceed.

## Returning URLs

As a rule, it's probably better practice to return absolute URIs from your Web APIs,
such as _http://example.com/foobar_, rather than returning relative URIs, such as _/foobar_.

**- reverse**

Signature: _reverse(viewname, \*args, \*\*kwargs)_

Has the same behavior as django.urls.reverse, except that it returns a fully qualified URL,
using the request to determine the host and port.
