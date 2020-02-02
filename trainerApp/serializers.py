from rest_framework import serializers
from .models import TrainerBio, TrainerRatingsAndReviews


class TrainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainerBio
        fields = "__all__"


class RatingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainerRatingsAndReviews
        fields = '__all__'


class RatingsSerializerWD(serializers.ModelSerializer):

    class Meta:
        model = TrainerRatingsAndReviews
        fields = '__all__'

        depth = 1