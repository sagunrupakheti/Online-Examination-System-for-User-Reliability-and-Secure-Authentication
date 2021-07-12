import django_filters
from .models import*

class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfileInfo
        fields = ['course_id']

class ExamFilter(django_filters.FilterSet):
    class Meta:
        model = Examination
        fields = ['course_code']


