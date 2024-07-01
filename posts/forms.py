from django import forms
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ["title","content","banner"]


class CommentsForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ["content"]