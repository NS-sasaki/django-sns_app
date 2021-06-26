from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        # imageフィールドを追加
        fields = (
            'content','image' 
        )
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 5, 'cols': 30,
                'placeholder': 'ここに入力してください'}
            ),
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'content','image'
        )
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 5, 'cols': 30}
            ),
        }

