import django_filters

from product.models import Category


class CategoryFilter(django_filters.FilterSet):
    parent = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Category
        fields = ['parent']
