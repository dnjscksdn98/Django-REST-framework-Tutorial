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
