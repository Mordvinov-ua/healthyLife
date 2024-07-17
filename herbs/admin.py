from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','time_create','time_update','is_published')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('is_published',)
    list_filter = ('time_create','time_update','is_published',)
    prepopulated_fields = {"slug":("name",)}

admin.site.register(Category, CategoryAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name','category','time_create','time_update','is_published')
    list_display_links = ('name','category',)
    search_fields = ('name','category',)
    list_editable = ('is_published',)
    list_filter = ('category','time_create','time_update','is_published',)
    prepopulated_fields = {"slug":("name",)}

admin.site.register(Group, GroupAdmin)

class TovarAdmin(admin.ModelAdmin):
    list_display = ('title','group','time_create','time_update','is_published',)
    list_display_links = ('title','group',)
    search_fields = ('title','group','sale_category',)
    list_editable = ('is_published',)
    list_filter = ('group','time_create','time_update','is_published','sale_category')
    prepopulated_fields = {"slug":("title",)}

admin.site.register(Tovar, TovarAdmin)

class Sale_categoryAdmin(admin.ModelAdmin):
    list_display = ('name','time_create','time_update','is_published')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('is_published',)
    list_filter = ('time_create','time_update','is_published',)
    prepopulated_fields = {"slug":("name",)}

admin.site.register(Sale_category, Sale_categoryAdmin)

'''class Sale_tovarAdmin(admin.ModelAdmin):
    list_display = ('title','sale_category','time_create','time_update','is_published')
    list_display_links = ('title','sale_category',)
    search_fields = ('title','sale_category',)
    list_editable = ('is_published',)
    list_filter = ('sale_category','time_create','time_update','is_published',)
    prepopulated_fields = {"slug":("title",)}

admin.site.register(Sale_tovar, Sale_tovarAdmin)'''
