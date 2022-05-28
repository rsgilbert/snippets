from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from snippets.serializers import SnippetSerializer



@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or creatte a new snippet
    To list: http :8000/snippets/
    To create: http POST :8000/snippets/ title=Jackson code="try:pass except:pass"
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print(f'Data is {data}')
        serializer = SnippetSerializer(data=data)
        print(f'Initial data is {serializer.initial_data}')
        if serializer.is_valid():
            print(f'Validated data is {serializer.validated_data}')
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return HttpResponse(status=400)


# @csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a single snippet by primary key
    To retrieve: http :8000/snippets/2      
    To replace/put: http PUT :8000/snippets/2 language=java code="if else" 
    To delete: http DELETE :8000/snippets/2
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        print(request) 
        print(type(request))
        data = JSONParser().parse(request)
        print(f'put data {data}')
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
    else: 
        return HttpResponse(status=400)
    