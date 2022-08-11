from django.forms import DateInput
from django_filters import rest_framework as filters
from django_filters.widgets import RangeWidget, DateRangeWidget

from gamenews_app.models import Post, Category, Author


class PostFilterApi(filters.FilterSet):
    categorys = filters.ModelMultipleChoiceFilter(
        field_name='categorys__name',
        queryset=Category.objects.all(),
    )
    # date_time = filters.RangeFilter()
    # date_time = filters.DateFilter(field_name='date_time',
    #                                widget=DateInput(format="%d.%m.%Y", attrs={'type': 'date'}))
    date_time = filters.DateFromToRangeFilter(
        field_name='date_time',
        widget=DateRangeWidget(attrs={'type': 'date'})
    )
    author = filters.ModelChoiceFilter(queryset=Author.objects.all())


    class Meta:
        model = Post
        fields = ['categorys', 'date_time']
