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
