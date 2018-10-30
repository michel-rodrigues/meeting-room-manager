import django_filters

from .models import ScheduleItem


class ScheduleItemFilter(django_filters.FilterSet):
    start = django_filters.CharFilter(field_name='start', lookup_expr='date')
    room = django_filters.CharFilter(
        field_name='room',
        lookup_expr='name__icontains',
    )

    class Meta:
        model = ScheduleItem
        fields = ('start', 'room')
