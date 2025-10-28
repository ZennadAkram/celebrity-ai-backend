# filters.py
import django_filters
from .models import Celebrity

class CelebrityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # partial match
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    is_Private = django_filters.BooleanFilter(field_name='is_Private')
    category = django_filters.NumberFilter(field_name='category__id')  # filter by category id
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')  # filter by category name


    class Meta:
        model = Celebrity
        fields = ['name', 'created_after', 'created_before', 'category', 'category_name', 'is_Private']
