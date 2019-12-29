from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserType, UserExtension, Carousel, ContactModel, Gallery, SubscriptionPlan, BMRValues, FindTrainer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name")


class UserTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserType
        fields = ["user_type"]


class UserTypeUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserType
        fields = "__all__"


class UserExtensionSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # user_type = UserTypeSerializer()

    class Meta:

        model = UserExtension
        fields = '__all__'

        depth = 1


class UserExtensionUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserExtension
        fields = "__all__"

        def to_representation(self, value):
            response = super().to_representation(value)
            response['user_type'] = UserTypeSerializer(value.user_type).data
            return response


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactModel
        fields = "__all__"


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = ['id', 'gallery_images']


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class BMRCalculatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserExtension
        fields = ['gender', 'height', 'weight', 'age', 'bmr_value']


class BMRValuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = BMRValues
        fields = '__all__'


class FindTrainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = FindTrainer
        fields = '__all__'


