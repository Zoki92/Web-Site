from django import forms
from .models import Comment
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    comment_content = forms.CharField(label="Comment:",
                                      widget=forms.Textarea(attrs={'rows': '3', 'cols': '15',
                                                                   'placeholder': 'Enter text...'}))
    class Meta:
        model = Comment
        fields = ['comment_content']
