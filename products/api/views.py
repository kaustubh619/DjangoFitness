from rest_framework import generics
from products.models import Products, Categories, subCategories, sub_subCategories
from .serializer import BlogPostSerializer, productCreateSerializer, CategoriesSerializer, Sub_CategoriesSerializer, subSub_CategoriesSerializer, BlogPostSerializerExtra, ProductUpdateSerializer, CategoryIdSerializer, ProductWithPaginationSerializer, ProductByCat
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .pagination import PostLimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

import os

from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


class ProjectCreateView(generics.CreateAPIView):
    # http_method_names = ['post']
    #
    # lookup_field            =  'slug' # slug, id
    queryset = Products.objects.all()
    serializer_class = productCreateSerializer

    def get_serializer_context(self):
        print("dsds")
        print(self.request.FILES)

    # permission_classes = ('AllowAny')

    # def get_queryset(self):
    #     return Products.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)


class ProjectUploadImage(APIView):
    # http_method_names = ['post']
    #
    # lookup_field            =  'slug' # slug, id
    # queryset = Products.objects.all()
    # serializer_class = productCreateSerializer

    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        print("dsds")
        print(self.request.FILES)

    def post(self, request, format=None):
        print(self.request.FILES)

        response_data = {}
        response_data['filename'] = handle_uploaded_file(self.request.FILES['file[0]'])
        response_data['message'] = 'success'
        response_data['status'] = '200'    

        return Response(response_data, status=status.HTTP_201_CREATED)
    
 

    # permission_classes = ('AllowAny')

    # def get_queryset(self):
    #     return Products.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)

def handle_uploaded_file(f):  

    if not os.path.isdir("media/products/"):
        os.makedirs("media/products/")


    with open('media/products/'+f.name, 'wb+') as destination:  
            for chunk in f.chunks():  
                destination.write(chunk) 

    return f.name
           

class ProjectListView(generics.RetrieveAPIView):
    http_method_names = ['get']
#
    lookup_field = 'slug'  # slug, id
    # queryset                = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    # permission_classes = ('AllowAny')

    def get_queryset(self):
        return Products.objects.select_related('category')

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)

class ProjectIDListView(generics.RetrieveAPIView):
#
    lookup_field = 'pk'  # slug, id
    # queryset                = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    # permission_classes = ('AllowAny')

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Products.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)

class ProjectUserListView(generics.ListAPIView):
#
    lookup_field = 'seller_id'  # slug, id
    # queryset                = BlogPost.objects.all()
    serializer_class = productCreateSerializer
    # permission_classes = ('AllowAny')

    def get_queryset(self):
        pk = self.kwargs.get("seller_id")
        return Products.objects.filter(seller_id=pk)

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)


class ProjectListViewDelete(generics.DestroyAPIView):
    #
    lookup_field = 'pk'  # slug, id
    # queryset                = Products.objects.all()
    serializer_class = BlogPostSerializer
    # permission_classes = ('AllowAny')

    def get_queryset(self):
        return Products.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        response_data = {}
        response_data['message'] = 'success'
        response_data['status'] = '200'
        self.perform_destroy(instance)
        return Response(response_data, status=status.HTTP_200_OK)

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)


class ProjectAllListView(generics.ListAPIView):
    #
    # lookup_field            = 'pk' # slug, id
    queryset = Products.objects.all()
    serializer_class = BlogPostSerializerExtra
    # permission_classes = ('AllowAny')


    def get_queryset(self):
        return Products.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)


class CategoriesListView(generics.ListCreateAPIView):
    #
    # lookup_field            = 'pk' # slug, id
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    # permission_classes = ('AllowAny')

    # def get_queryset(self):
    #     return BlogPost.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)


class CategoriesDeleteView(generics.DestroyAPIView):
    #
    lookup_field = 'pk'  # slug, id
    # queryset                = Products.objects.all()
    serializer_class = Categories
    # permission_classes = ('AllowAny')

    def get_queryset(self):
        return Categories.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        response_data = {}
        response_data['message'] = 'success'
        response_data['status'] = '200'
        self.perform_destroy(instance)
        return Response(response_data, status=status.HTTP_200_OK)




class Sub_CategoriesListView(generics.ListCreateAPIView):
    #
    lookup_field = 'category'  # slug, id
    serializer_class = Sub_CategoriesSerializer

    def get_queryset(self):
        pk = self.kwargs.get("category")
        print("pk")
        print(pk)
        return subCategories.objects.filter(category=pk)
    # permission_classes = ('AllowAny')

    # def get_queryset(self):
    #     return BlogPost.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)

class Sub_CategoriesListOnlyView(generics.ListAPIView):
    #
    # lookup_field = 'category'  # slug, id
    queryset = subCategories.objects.all()
    serializer_class = Sub_CategoriesSerializer

    # def get_queryset(self):
    #     pk = self.kwargs.get("category")
    #     print("pk")
    #     print(pk)
    #     return subCategories.objects.filter(category=pk)
    # permission_classes = ('AllowAny')

    # def get_queryset(self):
    #     return BlogPost.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)

class Sub_CategoriesDeleteView(generics.DestroyAPIView):
    #
    lookup_field = 'pk'  # slug, id
    # queryset                = Products.objects.all()
    serializer_class = Sub_CategoriesSerializer
    # permission_classes = ('AllowAny')

    def get_queryset(self):
        return subCategories.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        response_data = {}
        response_data['message'] = 'success'
        response_data['status'] = '200'
        self.perform_destroy(instance)
        return Response(response_data, status=status.HTTP_200_OK)

class subSub_CategoriesListView(generics.ListCreateAPIView):
    #
    lookup_field = 'category'  # slug, id
    # queryset = sub_subCategories.objects.all()
    serializer_class = subSub_CategoriesSerializer

    def get_queryset(self):
        pk = self.kwargs.get("category")
        return sub_subCategories.objects.filter(id=pk)

    # permission_classes = ('AllowAny')

    # def get_queryset(self):
    #     return BlogPost.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)


class subSub_CategoriesListOnlyView(generics.ListAPIView):
    #
    queryset = sub_subCategories.objects.all()
    serializer_class = subSub_CategoriesSerializer


    # permission_classes = ('AllowAny')

    # def get_queryset(self):
    #     return BlogPost.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)

class subSub_CategoriesDeleteView(generics.DestroyAPIView):
    #
    lookup_field = 'pk'  # slug, id
    # queryset                = Products.objects.all()
    serializer_class = subSub_CategoriesSerializer
    # permission_classes = ('AllowAny')

    def get_queryset(self):
        return sub_subCategories.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        response_data = {}
        response_data['message'] = 'success'
        response_data['status'] = '200'
        self.perform_destroy(instance)
        return Response(response_data, status=status.HTTP_200_OK)


    # permission_classes = ('AllowAny')

    # def get_queryset(self):
    #     return BlogPost.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)

class Product(APIView):

    def get_object(self, pk):
        try:
            return Products.objects.get(id=pk)
        except Products.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        product_obj = self.get_object(pk)
        serializer = ProductUpdateSerializer(product_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(generics.RetrieveAPIView):

    lookup_field = 'pk'
    serializer_class = CategoryIdSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Categories.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return User.objects.all(pk=pk)


class CategoryUpdate(APIView):
    def get_object(self, pk):
        try:
            return Categories.objects.get(id=pk)
        except id.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        user_ext = self.get_object(pk)
        serializer = CategoryIdSerializer(user_ext, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryAdd(viewsets.ViewSet):

    def category_list(self, request):
        queryset = CategoriesSerializer.objects.all()
        serializer = CategoriesSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategory(APIView):
    def get_object(self, pk):
        try:
            return subCategories.objects.get(id=pk)
        except id.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        subcategory = self.get_object(pk)
        SubCategory = Sub_CategoriesSerializer(subcategory)
        return Response(SubCategory.data)

    def put(self, request, pk, format=None):
        user_ext = self.get_object(pk)
        serializer = Sub_CategoriesSerializer(user_ext, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryAdd(viewsets.ViewSet):

    def subcategory_list(self, request):
        queryset = Sub_CategoriesSerializer.objects.all()
        serializer = Sub_CategoriesSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = Sub_CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Brand(APIView):
    def get_object(self, pk):
        try:
            return sub_subCategories.objects.get(id=pk)
        except id.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        brand = self.get_object(pk)
        Brand = subSub_CategoriesSerializer(brand)
        return Response(Brand.data)

    def put(self, request, pk, format=None):
        brand = self.get_object(pk)
        serializer = subSub_CategoriesSerializer(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductByPagination(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductWithPaginationSerializer
    pagination_class = PostLimitOffsetPagination


class ProductsByCategory(generics.ListAPIView):

    def get_object(self, pk):
        try:
            return Products.objects.filter(category=pk)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        Product = ProductByCat(product, many=True, context={"request": request})
        return Response(Product.data)


def handle_uploaded_file(f):
    if not os.path.isdir("media/product_images/"):
        os.makedirs("media/product_images/")

    with open('media/product_images/'+f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    return f.name


@permission_classes((AllowAny,))
class ProductUploadImage(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        print(self.request.FILES)

    def post(self, request, format=None):
        res = {}

        for i in self.request.FILES:
            array = {}
            array['success'] = 1
            res['url'] = 'http://www.mytruestrength.com/backend/media/product_images/' + handle_uploaded_file(self.request.FILES[i])
            array['file'] = res
        return Response(array)


@permission_classes((AllowAny,))
class GetProductById(generics.ListAPIView):
    def get_object(self, slug):
        try:
            return Products.objects.get(slug=slug)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        obj = self.get_object(slug)
        Obj = ProductByCat(obj, context={"request": request})
        return Response(Obj.data)         

