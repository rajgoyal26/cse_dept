from .models import Project
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model=Project
        fields=['added_by' , 'supervisor']