from rest_framework import serializers
from products.models import Products, Categories, subCategories,  sub_subCategories
from django.contrib.auth.models import User



class CategoriesSerializer(serializers.ModelSerializer):


    class Meta:
        model = Categories
        fields = '__all__'
        

class Sub_CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = subCategories
        fields = '__all__' 
        


class subSub_CategoriesSerializer(serializers.ModelSerializer):


    class Meta:
        model = sub_subCategories
        fields = '__all__' 
        


class BlogPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__' 
        depth = 1



class BlogPostSerializerExtra(serializers.ModelSerializer):


    class Meta:
        model = Products
        
        fields = '__all__' 
        # depth = 1
        

class productCreateSerializer(serializers.ModelSerializer):

    def validate(self, data):
        print(data)
    
        return data

    class Meta:
        model = Products
        fields = '__all__'


class ProductUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'


class CategoryIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'
        depth = 1


class ProductWithPaginationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        depth = 1


class ProductByCat(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        depth = 1

