from django.forms.models import ModelForm
from .models import Podcast,PodcastComment
from django.utils import translation
class PodcastForm(ModelForm):
    class Meta:
        model = Podcast
        fields = ['title','description','banner','audio']

    def __init__(self,*args, **kwargs):
        super(PodcastForm, self).__init__(*args, **kwargs)
        if translation.get_language() == 'fa':
            for field in self.fields.values():
                field.widget.attrs.update({'dir': 'rtl'})
        else:
            for field in self.fields.values():
                field.widget.attrs.update({'dir': 'ltr'})



class PodcastCommentForm(ModelForm):
    class Meta:
        model = PodcastComment
        fields = ['content']

    def __init__(self,*args,**kwargs):
        super(PodcastCommentForm,self).__init__(*args,**kwargs)
        if translation.get_language() == 'fa':
            for field in self.fields.values():
                field.widget.attrs.update({'dir': 'rtl'})
        else:
            for field in self.fields.values():
                field.widget.attrs.update({'dir': 'ltr'})


