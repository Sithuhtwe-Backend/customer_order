import imp
import django_filters
from django_filters import DateFilter
from .models import *
class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="created_at",lookup_expr="gte") #gte = greater than or equal
    end_date = DateFilter(field_name="created_at",lookup_expr="lte") #lte = less than or equal
    class Meta:
        model = Order
        fields = ['product','status','start_date','end_date']