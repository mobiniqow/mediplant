from django_filters import rest_framework as filters


class ProductFilter(drf_filters.FilterSet):
    name = drf_filters.CharFilter(field_name='name', lookup_expr='icontains')
    type = drf_filters.ChoiceFilter(choices=Product.Type.choices)
    material = drf_filters.ChoiceFilter(choices=Product.Material.choices)
    state = drf_filters.ChoiceFilter(choices=Product.State.choices)
    is_active = drf_filters.BooleanFilter(field_name='is_active')
    category = drf_filters.CharFilter(field_name='category__name', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['name', 'type', 'material', 'state', 'is_active', 'category']
