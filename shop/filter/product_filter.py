import django_filters

from  sale.models import ShopProduct


class ShopProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    material = django_filters.ChoiceFilter(field_name='material', choices=ShopProduct.Material.choices)
    product = django_filters.NumberFilter(field_name='product')
    shop = django_filters.NumberFilter(field_name='shop')

    class Meta:
        model = ShopProduct
        fields = ['price_min', 'price_max', 'material', 'product', 'shop']