from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post



class NewsFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'heading': ['icontains'],
            # количество товаров должно быть больше или равно
            'text': ['icontains'],
        }