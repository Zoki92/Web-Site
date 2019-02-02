from django.shortcuts import render
from blog.models import Post, Tag
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.core import serializers



def search_view_django(request):
    search_query = request.GET.get('q', None)

    if search_query is not None:
        data_search = Post.django_posts.search(search_query)
    else:
        data_search = {}
    data = serializers.serialize('json', data_search)
    return JsonResponse(data, safe=False)

def search_view_lifestyle(request):
    search_query = request.GET.get('q', None)
    if search_query is not None:
        data_search = Post.lifestyle_posts.search(search_query)
    else:
        data_search = {}
    data = serializers.serialize('json', data_search)
    return JsonResponse(data, safe=False)



