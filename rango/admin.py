from django.contrib import admin

from rango.models import Category, Page, UserProfile
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'views', 'likes']

class PageAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'url', 'views']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)