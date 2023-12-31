from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_category',
            'post_title',
            'post_text'
        ]

    def clean(self):
        cleaned_data = super().clean()
        post_title = cleaned_data.get("post_title")
        if post_title is not None and len(post_title) < 10:
            raise ValidationError({
                "post_title": "Название не может быть меньше 10 символов."
            })
        post_text = cleaned_data.get('post_text')
        if post_text == post_title:
            raise ValidationError(
                "Название не должно совпадать с текстом статьи."
            )
        return cleaned_data
