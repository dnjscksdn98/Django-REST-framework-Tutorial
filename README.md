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
