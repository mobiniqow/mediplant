from rest_framework import serializers
from encyclopedia.models import EncyclopediaCombinedDrugs, EncyclopediaCombinedDrugsImage, EncyclopediaOfDiseases, \
    EncyclopediaOfDiseasesImage, ArticleReference, EncyclopediaOfDiseasesArticle, EncyclopediaOfDiseasesReference, \
    HerbalEncyclopediaImage, HerbalEncyclopediaArticle, HerbalEncyclopediaReference, HerbalEncyclopedia, Hashtag, \
    Comment, News
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
        fields = "__all__"


class EncyclopediaOfDiseasesImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncyclopediaOfDiseasesImage

        fields = ['image']

class ArticleEncyclopediaDiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleEncyclopedia
        fields = "__all__"

class ArticleReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleReference
        fields = "__all__"

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

# giahan
class HerbalEncyclopediaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HerbalEncyclopediaImage
        fields = ['image']

class HerbalEncyclopediaArticleSerializer(serializers.ModelSerializer):
    article = ArticleEncyclopediaSerializer()

    class Meta:
        model = HerbalEncyclopediaArticle
        fields = ['article']


class HerbalEncyclopediaReferenceSerializer(serializers.ModelSerializer):
    refrence = ArticleReferenceSerializer()

    class Meta:
        model = HerbalEncyclopediaReference
        fields = ['refrence']


class HerbalEncyclopediaSerializer(serializers.ModelSerializer):
    images = HerbalEncyclopediaImageSerializer(source='herbalencyclopediaimage_set', many=True, read_only=True)
    articles = HerbalEncyclopediaArticleSerializer(source='herbalencyclopediaarticle_set', many=True, read_only=True)
    references = HerbalEncyclopediaReferenceSerializer(source='herbalencyclopediareference_set', many=True, read_only=True)

    class Meta:
        model = HerbalEncyclopedia
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(f"Articles: {representation.get('articles')}")
        return representation

# serializer
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['name','id']

class CommentSerializer(serializers.ModelSerializer):
    recomments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user_name', 'email', 'message', 'status', 'created_at', 'recomments']

    def get_recomments(self, obj):
        recomments = obj.recomments.filter(status='active')
        return CommentSerializer(recomments, many=True).data

class NewsSerializer(serializers.ModelSerializer):
    hashtags = HashtagSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'excerpt', 'image', 'created_at', 'updated_at', 'hashtags', 'comments']

class NewsListSerializer(serializers.ModelSerializer):
    hashtags = serializers.StringRelatedField(many=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'excerpt', 'image', 'created_at', 'updated_at', 'hashtags', 'comment_count']

    def get_comment_count(self, obj):
        return Comment.objects.filter(news=obj, status='active').count()