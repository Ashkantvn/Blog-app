from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . import models
from django.utils import translation


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ["title","content","banner"]

    def __init__(self,*args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if translation.get_language() == 'fa':
                for field in self.fields.values():
                    field.widget.attrs.update({'dir': 'rtl'})
            else:
                for field in self.fields.values():
                    field.widget.attrs.update({'dir': 'ltr'})


class CommentsForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ["content"]

    def __init__(self,*args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if translation.get_language() == 'fa':
                for field in self.fields.values():
                    field.widget.attrs.update({'dir': 'rtl'})
            else:
                for field in self.fields.values():
                    field.widget.attrs.update({'dir': 'ltr'})
    