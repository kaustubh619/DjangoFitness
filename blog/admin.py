from django.contrib import admin
from .models import BlogCategory, BlogPost, BlogComment


class BlogPostAdmin(admin.ModelAdmin):
    ordering = ('id',)
    exclude = ('slug',)


admin.site.register(BlogCategory)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogComment)
