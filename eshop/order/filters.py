from django_filters import rest_framework as filters

from .models import Order


class OrderFilter(filters.FilterSet):
    keyword = filters.CharFilter(field_name='name', lookup_expr="icontains")
    min_amount = filters.NumberFilter(
        field_name='total_amount' or 0, lookup_expr="gte")

    class Meta:
        model = Order
        fields = ('payment_mode', 'status',
                  'payment_status', 'keyword', 'min_amount')
