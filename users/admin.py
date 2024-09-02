from django.contrib import admin
from .models import Contact
# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['created_date','subject','content','user']
    
    
    empty_value_display = '--Empty--'
