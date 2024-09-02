from django.contrib import admin
from . import models
from django.utils.timezone import now

#actions
def make_status_true(modeladmin, request, queryset):
    queryset.update(status=True)
    make_status_true.short_description = "Mark selected items as True"

def make_status_false(modeladmin, request, queryset):
    queryset.update(status=False)
    make_status_true.short_description = "Mark selected items as False"

def set_published_date_to_now(modeladmin, request, queryset):
    queryset.update(published_date = now())
    set_published_date_to_now.short_description = "Set published date to current datetime"
    
def make_premium_true(modeladmin, request, queryset):
    queryset.update(premium=True)
    make_premium_true.short_description = "Mark premium selected items as True"

def make_premium_false(modeladmin, request, queryset):
    queryset.update(premium=False)
    make_premium_true.short_description = "Mark premium selected items as False"



    
# Register your models here.
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["pk",'title','author', "published_date", "status",'premium',"counted_views","date_created","update_date"]
    summernote_fields = ('content')
    actions = [make_status_true,make_status_false,set_published_date_to_now,make_premium_false,make_premium_true]

admin.site.register(models.Comment)
admin.site.register(models.FavoritePost)
admin.site.register(models.Category)