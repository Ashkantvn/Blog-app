from django import forms
from .models import Contact
from django.utils import translation

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["subject","content","email"]

    def __init__(self,*args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        if translation.get_language() == 'fa':
            for field in self.fields.values():
                field.widget.attrs.update({'dir': 'rtl'})
        else:
            for field in self.fields.values():
                field.widget.attrs.update({'dir': 'ltr'})