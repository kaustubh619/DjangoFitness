from rest_framework import serializers
from cart.models import Cart


class CartCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('cart_key',)


class CartListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'

        depth = 2


class CartQuantitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['quantity']
