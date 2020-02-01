from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import BlogCategory, BlogPost, BlogComment
from .serializers import BlogCategorySerializer, BlogPostSerializer, BlogCommentSerializer, BlogPostLikeSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from django.http import HttpResponse, Http404
from rest_framework import status
from .pagination import PostLimitOffsetPagination


@permission_classes((AllowAny,))
class BlogCategoryView(viewsets.ViewSet):
    def cat_list(self, request):
        queryset = BlogCategory.objects.all()
        serializer = BlogCategorySerializer(queryset, many=True)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class BlogPostView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    pagination_class = PostLimitOffsetPagination


@permission_classes((AllowAny,))
class BlogPostViewWithoutPagination(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


@permission_classes((AllowAny,))
class BlogByCategory(generics.ListAPIView):

    def get_object(self, pk):
        try:
            return BlogPost.objects.filter(category=pk)
        except BlogPost.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        blog = self.get_object(pk)
        Blog = BlogPostSerializer(blog, many=True, context={"request": request})
        return Response(Blog.data)


@permission_classes((AllowAny,))
class BlogCommentView(generics.ListAPIView):
    def get_object(self, pk):
        try:
            return BlogComment.objects.filter(blog=pk)
        except BlogComment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        blogcomment = self.get_object(pk)
        BlogComment = BlogCommentSerializer(blogcomment, many=True, context={"request": request})
        return Response(BlogComment.data)


@permission_classes((AllowAny,))
class BlogById(generics.ListAPIView):
    def get_object(self, slug):
        try:
            return BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        blog = self.get_object(slug)
        Blog = BlogPostSerializer(blog, context={"request": request})
        return Response(Blog.data)


class BlogCommentPostView(viewsets.ViewSet):
    def comment_list(self, request):
        queryset = BlogComment.objects.all()
        serializer = BlogCommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogPostLikeView(APIView):
    def get_object(self, slug):
        try:
            return BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        blog = self.get_object(slug)
        Blog = BlogPostLikeSerializer(blog)
        return Response(Blog.data)

    def put(self, request, slug):
        Blog = self.get_object(slug)
        serializer = BlogPostLikeSerializer(Blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)