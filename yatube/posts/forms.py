from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': "Пост",
            'group': "Группа",
        }
        help_texts = {
            'text': "Новый пост",
            'group': "Группа с новым постом",
        }
