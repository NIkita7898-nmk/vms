from django_filters import rest_framework as filters
from .models import PurchaseOrder


class PurchaseOrderFilter(filters.FilterSet):
    vendor = filters.NumberFilter(field_name="vendor_id")

    class Meta:
        model = PurchaseOrder
        fields = ["vendor"]
