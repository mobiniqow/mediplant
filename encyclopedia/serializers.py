from rest_framework import serializers
from encyclopedia.models import EncyclopediaCombinedDrugs, EncyclopediaCombinedDrugsImage, EncyclopediaOfDiseases, \
    EncyclopediaOfDiseasesImage, ArticleReference, EncyclopediaOfDiseasesArticle, EncyclopediaOfDiseasesReference
from rest_framework import serializers
from .models import ArticleEncyclopedia

class EncyclopediaCombinedDrugsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncyclopediaCombinedDrugsImage
        fields = ['image']

class EncyclopediaCombinedDrugsSerializer(serializers.ModelSerializer):
    images = EncyclopediaCombinedDrugsImageSerializer(many=True, source='encyclopediacombineddrugsimage_set')

    class Meta:
        model = EncyclopediaCombinedDrugs
        fields = [
            'id', 'name', 'classification', 'latin_name', 'bomi', 'created_at',
            'compounds', 'amount_of_compounds', 'indications', 'prohibited_usage',
            'complications', 'pregnancy', 'method_of_drug_production', 'how_to_use',
            'treatment_duration', 'pharmaceutical_supplements', 'the_nature_of_the_drug',
            'drug_manufacturing_company', 'images'
        ]

class ArticleEncyclopediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleEncyclopedia
        fields = ['id','name']


class EncyclopediaOfDiseasesImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncyclopediaOfDiseasesImage

        fields = ['image']

class ArticleEncyclopediaDiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleEncyclopedia
        fields = ['id', 'name']

class ArticleReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleReference
        fields = ['id', 'name']

class EncyclopediaOfDiseasesArticleSerializer(serializers.ModelSerializer):
    article = ArticleEncyclopediaSerializer()

    class Meta:
        model = EncyclopediaOfDiseasesArticle
        fields = ['article']

class EncyclopediaOfDiseasesReferenceSerializer(serializers.ModelSerializer):
    refrence = ArticleReferenceSerializer()

    class Meta:
        model = EncyclopediaOfDiseasesReference
        fields = ['refrence']

class EncyclopediaOfDiseasesSerializer(serializers.ModelSerializer):
    images = EncyclopediaOfDiseasesImageSerializer(source='encyclopediaofdiseasesimage_set', many=True, read_only=True)
    articles = EncyclopediaOfDiseasesArticleSerializer(source='encyclopediaofdiseasesarticle_set', many=True, read_only=True)
    references = EncyclopediaOfDiseasesReferenceSerializer(source='encyclopediaofdiseasesreference_set', many=True, read_only=True)

    class Meta:
        model = EncyclopediaOfDiseases
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(f"Articles: {representation.get('articles')}")
        return representation
