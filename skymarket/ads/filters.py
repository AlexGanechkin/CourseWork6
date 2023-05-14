import django_filters.rest_framework

from ads.models import Ad


class AdFilter(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Ad
        fields = ['title']
