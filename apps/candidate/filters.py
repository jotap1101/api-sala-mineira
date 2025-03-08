from .models import Candidate
import django_filters

class CandidateFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')

    date_of_birth = django_filters.DateFilter()
    day_of_birth = django_filters.NumberFilter(field_name='date_of_birth', lookup_expr='day')
    month_of_birth = django_filters.NumberFilter(field_name='date_of_birth', lookup_expr='month')
    year_of_birth = django_filters.NumberFilter(field_name='date_of_birth', lookup_expr='year')
    date_of_birth__gt = django_filters.DateFilter(field_name='date_of_birth', lookup_expr='gt')
    date_of_birth__lt = django_filters.DateFilter(field_name='date_of_birth', lookup_expr='lt')

    gender = django_filters.CharFilter(lookup_expr='icontains', field_name='gender__name')
    cpf = django_filters.CharFilter(lookup_expr='icontains')
    rg = django_filters.CharFilter(lookup_expr='icontains')
    has_disability = django_filters.BooleanFilter()
    has_drivers_license = django_filters.BooleanFilter()
    drivers_license_category = django_filters.CharFilter(lookup_expr='icontains', field_name='drivers_license_category__name')
    is_first_job = django_filters.BooleanFilter()
    is_currently_employed = django_filters.BooleanFilter()

    created_at = django_filters.DateTimeFilter()
    created_at__gt = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gt')
    created_at__lt = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lt')

    updated_at = django_filters.DateTimeFilter()
    updated_at__gt = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gt')
    updated_at__lt = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lt')

    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'cpf', 'rg', 'has_disability', 'has_drivers_license', 'drivers_license_category', 'is_first_job', 'is_currently_employed', 'created_at', 'updated_at']