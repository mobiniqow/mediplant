import django_filters as drf_filters
from product.models import Product, Category

class ProductFilter(drf_filters.FilterSet):
    name = drf_filters.CharFilter(field_name='name', lookup_expr='icontains')
    state = drf_filters.ChoiceFilter(choices=Product.State.choices)
    is_active = drf_filters.BooleanFilter(field_name='is_active')
    category = drf_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        field_name='category',
        to_field_name='id',
    )
    type = drf_filters.ModelMultipleChoiceFilter(
        queryset=Product.objects.all(),
        field_name='type',
        to_field_name='type',
    )

    class Meta:
        model = Product
        fields = ['name', 'type', 'state', 'is_active', 'category']
