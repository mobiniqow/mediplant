import django_filters as drf_filters
from product.models import Product, Category
from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import ValidationError
from collections import OrderedDict


class ProductFilter(drf_filters.FilterSet):
    name = drf_filters.CharFilter(field_name='name', lookup_expr='icontains')
    state = drf_filters.ChoiceFilter(choices=Product.State.choices)
    is_active = drf_filters.BooleanFilter(field_name='is_active')
    category = drf_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        field_name='category',
        to_field_name='id',
    )
    type = drf_filters.MultipleChoiceFilter(
        choices=Product. Type,  # فرض می‌کنیم که `TYPES_CHOICES` یک لیست از گزینه‌ها باشد
        field_name='type'
    )

    class Meta:
        model = Product
        fields = ['name', 'type', 'state', 'is_active', 'category']


class OrderingFilter(BaseFilterBackend):
    """
    Filter to allow ordering of queryset using the `ordering` query parameter.
    You can use this to filter by field names or reverse order with a "-" prefix.
    """

    def filter_queryset(self, request, queryset, view):
        ordering = request.query_params.get('ordering', None)
        if ordering is not None:
            ordering_fields = getattr(view, 'ordering_fields', None)
            if ordering_fields:
                ordering = ordering.split(',')
                for order in ordering:
                    if order.startswith('-'):
                        field = order[1:]
                        if field not in ordering_fields:
                            raise ValidationError(f"Cannot order by field {field}.")
                        queryset = queryset.order_by(*ordering)
                    else:
                        if order not in ordering_fields:
                            raise ValidationError(f"Cannot order by field {order}.")
                        queryset = queryset.order_by(*ordering)
        return queryset
