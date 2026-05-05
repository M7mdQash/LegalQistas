from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_published', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'created_at')
    prepopulated_fields = {"slug": ("title",)}