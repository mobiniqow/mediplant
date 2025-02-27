import django_filters

from product.models import Product
from sale.models import ShopProduct
from shop.models import Shop

TYPE_CHOICES_DICT = {label: value for value, label in Product.Type.choices}
class ProductTypeFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    def filter(self, qs, value):
        if not value:
            return qs
        try:
            # 🔥 تبدیل مقدارهای فارسی به مقدار عددی
            numeric_values = [TYPE_CHOICES_DICT[v] for v in value if v in TYPE_CHOICES_DICT]
            return qs.filter(product__type__in=numeric_values)
        except KeyError:
            return qs.none()
class ShopProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    material = django_filters.ChoiceFilter(field_name='material', choices=ShopProduct.Material.choices)
    product = django_filters.NumberFilter(field_name='product')
    shop = django_filters.NumberFilter(field_name='shop')
    product_name = django_filters.CharFilter(field_name='product__name', lookup_expr='icontains', label='نام محصول')
    shop_name = django_filters.CharFilter(field_name='shop__name', lookup_expr='icontains', label='نام فروشگاه')  # 🔥 اضافه شده
    product_type = ProductTypeFilter(field_name="product__type", lookup_expr="in", label="نوع محصول")

    class Meta:
        model = ShopProduct
        fields = ['price_min', 'price_max', 'material', 'product', 'shop', 'product_name', 'shop_name','product_type']



class ShopFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='نام فروشگاه')
    state = django_filters.ChoiceFilter(field_name='state', choices=Shop.ShopStatus.choices, label='وضعیت فروشگاه')
    rate_state = django_filters.ChoiceFilter(field_name='rate_state', choices=Shop.ShopRate.choices,
                                             label='وضعیت امتیاز')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='حداقل قیمت')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='حداکثر قیمت')
    shop_home = django_filters.CharFilter(field_name='shop_home', lookup_expr='icontains', label='آدرس فروشگاه')

    class Meta:
        model = Shop
        fields = ['name', 'state', 'rate_state', 'price_min', 'price_max', 'shop_home']
