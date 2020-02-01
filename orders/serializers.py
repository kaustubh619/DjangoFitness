from rest_framework import serializers
from .models import Orders, OrderSession


class OrderSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSession
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class EditOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['razorpay_signature', 'razorpay_payment_id', 'payment_status']
