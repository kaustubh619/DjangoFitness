from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .models import TrainerBio, TrainerRatingsAndReviews
from .serializers import TrainerSerializer, RatingsSerializer, RatingsSerializerWD
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from django.http import Http404
from django.db.models import Q


@permission_classes((AllowAny,))
class TrainerList(viewsets.ViewSet):

    def trainer_list(self, request):
        queryset = TrainerBio.objects.all()
        serializer = TrainerSerializer(queryset, many=True)
        return Response(serializer.data)


class AddTrainer(viewsets.ViewSet):

    def trainer_data(self, request):
        queryset = TrainerBio.objects.all()
        serializer = TrainerSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TrainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTrainer(APIView):
    def get_object(self, slug):
        try:
            return TrainerBio.objects.get(slug=slug)
        except TrainerBio.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        obj = self.get_object(slug)
        Obj = TrainerSerializer(obj)
        return Response(Obj.data)

    def put(self, request, slug):
        obj = self.get_object(slug)
        serializer = TrainerSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        obj = self.get_object(slug)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes((AllowAny,))
class GetTrainerBySlug(APIView):
    def get_object(self, slug):
        try:
            return TrainerBio.objects.get(slug=slug)
        except TrainerBio.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        obj = self.get_object(slug)
        Obj = TrainerSerializer(obj)
        return Response(Obj.data)


class RatingsPostView(viewsets.ViewSet):
    def ratings_list(self, request):
        queryset = TrainerRatingsAndReviews.objects.all()
        serializer = RatingsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RatingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingsPutView(APIView):
    def get_object(self, trainer, user):
        try:
            all_obj = TrainerRatingsAndReviews.objects.filter(Q(trainer=trainer) & Q(user=user))
            return all_obj
        except TrainerRatingsAndReviews.DoesNotExist:
            raise Http404

    def get(self, request, trainer, user):
        obj = self.get_object(trainer, user)
        Obj = RatingsSerializer(obj, context={"request": request}, many=True)
        return Response(Obj.data[0])


class UserRatingsPutView(APIView):
    def get_object(self, trainer, user):
        try:
            all_obj = TrainerRatingsAndReviews.objects.filter(user=user)
            filtered_obj = all_obj.filter(trainer=trainer)[0]
            return filtered_obj
        except TrainerRatingsAndReviews.DoesNotExist:
            raise Http404

    def get(self, request, trainer, user):
        obj = self.get_object(trainer, user)
        Obj = RatingsSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, trainer, user):
        obj = self.get_object(trainer, user)
        serializer = RatingsSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class UserTrainerReviews(APIView):
    def get_object(self, pk):
        try:
            return TrainerRatingsAndReviews.objects.filter(trainer=pk)
        except TrainerRatingsAndReviews.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = RatingsSerializerWD(obj, context={"request": request}, many=True)
        return Response(Obj.data)
