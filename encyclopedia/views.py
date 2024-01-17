from django.shortcuts import render
from encyclopedia.models import ArticleEncyclopedia
from encyclopedia.pagination import StandardResultsSetPagination
from encyclopedia.serializers import ArticleEncyclopediaSerializer
from rest_framework import generics


class BlogsAPIView(generics.ListAPIView):
    queryset = ArticleEncyclopedia.objects.all()
    serializer_class = ArticleEncyclopediaSerializer
    # pagination_class = StandardResultsSetPagination






