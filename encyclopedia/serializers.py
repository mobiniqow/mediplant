from rest_framework import serializers

from encyclopedia.models import ArticleEncyclopedia


class ArticleEncyclopediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleEncyclopedia
        fields = '__all__'
