from django.contrib import admin

# Register your models here.
from .models import Category
from .models import Location
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "pub_date", "location"]
    search_fields = ["title", "author", "category", "pub_date", "location"]
    list_filter = ["title", "author", "category", "pub_date", "location"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']
    list_filter = ['title', 'description']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_published', 'created_at']
    search_fields = ['name', 'is_published', 'created_at']
    list_filter = ['name', 'is_published', 'created_at']
