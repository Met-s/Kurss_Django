from django.forms import DateInput
from django_filters import (
    FilterSet, CharFilter, ModelMultipleChoiceFilter, DateFilter,
)
from .models import Category


class PostFilter(FilterSet):
    name = CharFilter(
        field_name='post_title',
        label='Название статьи',
        lookup_expr='icontains'
    )

    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category_through',
        queryset=Category.objects.all(),
        label='Категория',
        conjoined=True,
    )

    data = DateFilter(
        field_name='post_date',
        lookup_expr='gt',
        label='Позже указанной даты',
        widget=DateInput(attrs={'type': 'date'})
    )
