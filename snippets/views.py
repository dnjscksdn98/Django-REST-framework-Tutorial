from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer


@csrf_exempt
def snippet_list(request):
    # list all code snippets, or create a new snippet
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        # any object can be passed for serialization (otherwise only dict instances are allowed)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            # 201 Created : The request has been fulfilled, resulting in the creation of a new resource.
            return JsonResponse(serializer.data, status=201)

        # 400 Bad Request : The server cannot or will not process the request due to an apparent client error
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    # Retrieve, update, or delete a code snippet
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        snippet.delete()
        # 204 No Content : The server successfully processed the request and is not returning any content.
        return HttpResponse(status=204)
