from django import forms
from .models import Post

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'position',
            'author',
            'category',
            'category',
            'heading',
            'text',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле quantity из формы, чтобы оно не отображалось и не было доступно для редактирования
        self.fields['position'].widget = forms.HiddenInput()
        self.fields['position'].initial = 'NE'


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'position',
            'author',
            'category',
            'category',
            'heading',
            'text',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле quantity из формы, чтобы оно не отображалось и не было доступно для редактирования
        self.fields['position'].widget = forms.HiddenInput()
        self.fields['position'].initial = 'AR'

