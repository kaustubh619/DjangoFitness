from rest_framework import serializers
from .models import BlogCategory, BlogPost, BlogComment


class BlogCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogCategory
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('id', 'added_by', 'category', 'title', 'content', 'blog_img', 'posted_on', 'slug', 'likes', 'blog_comments')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        depth = 1


class BlogCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogComment
        fields = '__all__'


class BlogPostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('likes', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }







