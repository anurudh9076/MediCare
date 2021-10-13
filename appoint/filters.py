import django_filters

from .models import Doctor

class DoctorFilter(django_filters.FilterSet):
    class meta:
        model = Doctor
        fields = [ 'city', 'speciality']
