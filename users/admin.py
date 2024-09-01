from django.contrib import admin
from .models import Contact
# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['created_date','subject','content','user']
    
    
    @admin.display(empty_value='-empty-', ordering='subject')
    def view_subject(self, obj):
        return obj.subject if obj.subject else None
    
    view_subject.empty_value_display = '-empty-'
