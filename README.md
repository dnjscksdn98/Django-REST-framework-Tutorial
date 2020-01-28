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
