from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer, UserTypeSerializer, UserTypeUpdateSerializer, UserExtensionSerializer, \
    UserExtensionUpdateSerializer, CarouselSerializer, ContactSerializer, GallerySerializer, SubscriptionSerializer, \
    BMRCalculatorSerializer, BMRValuesSerializer, FindTrainerSerializer, CouponSerializer, UserSubscriptionSerializer
from django.http import HttpResponse, Http404
from rest_framework import viewsets, generics, status
from .models import UserType, UserExtension, Carousel, ContactModel, Gallery, SubscriptionPlan, BMRValues, FindTrainer, Coupon, UserSubscription
from twilio.rest import Client
import os
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_admin(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    user_ext = UserExtension.objects.get(user=user)

    if not user or str(user_ext.user_type) != 'Admin':
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    user = User.objects.get(username=user)
    return Response({'token': token.key, 'user': user.id, 'username': user.username},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_customer(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    user_ext = UserExtension.objects.get(user=user)

    if not user or str(user_ext.user_type) != 'Customer':
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    user = User.objects.get(username=user)
    return Response({'token': token.key, 'user': user.id, 'username': user.username},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    first_name = request.data.get("first_name")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)

    user = User()

    user.username = username
    user.email = email
    user.first_name = first_name
    user.set_password(password)
    user.save()
    Token.objects.get_or_create(user=user)
    return Response({'user_id': user.id},
                    status=HTTP_200_OK)


class UserListView(viewsets.ViewSet):
    def userList(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        User = self.get_object(pk)
        User.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserExtensionListView(viewsets.ViewSet):

    def userExtList(self, request):
        queryset = UserExtension.objects.filter(user_type=1)
        serializer = UserExtensionSerializer(queryset, many=True)
        return Response(serializer.data)


class UserUpdateDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        User = UserSerializer(user)
        return Response(User.data)

    def put(self, request, pk, format=None):
        User = self.get_object(pk)
        serializer = UserSerializer(User, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        User = self.get_object(pk)
        User.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes((AllowAny,))
class UserExtensionPostView(viewsets.ViewSet):

    def user_extension_list(self, request):
        queryset = UserExtension.objects.all()
        serializer = UserExtensionUpdateSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserExtensionUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_extension = self.get_object(pk)
        user_extension.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserTypePostView(viewsets.ViewSet):

    def user_type_list(self, request):
        queryset = UserType.objects.all()
        serializer = UserTypeUpdateSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserTypeUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_type = self.get_object(pk)
        user_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserTypeListView(viewsets.ViewSet):

    def userTypeList(self, request):
        queryset = UserType.objects.all()
        serializer = UserTypeSerializer(queryset, many=True)
        return Response(serializer.data)


class TrainerListView(viewsets.ViewSet):
    def userTrainerList(self, request):
        queryset = UserExtension.objects.filter(user_type=2)
        serializer = UserExtensionSerializer(queryset, many=True)
        return Response(serializer.data)


class CustomerListView(viewsets.ViewSet):
    def userCustomerList(self, request):
        queryset = UserExtension.objects.filter(user_type=3)
        serializer = UserExtensionSerializer(queryset, many=True)
        return Response(serializer.data)


class UserExt(APIView):
    def get_object(self, pk):
        try:
            return UserExtension.objects.get(user=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_ext = self.get_object(pk)
        User_ext = UserExtensionSerializer(user_ext)
        return Response(User_ext.data)

    def put(self, request, pk, format=None):
        user_ext = self.get_object(pk)
        serializer = UserExtensionUpdateSerializer(user_ext, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarouselImageUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

      carousel_serializer = CarouselSerializer(data=request.data)

      if carousel_serializer.is_valid():
          carousel_serializer.save()
          return Response(carousel_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(carousel_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class ImageView(generics.ListAPIView):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer


@permission_classes((AllowAny,))
class ContactListView(viewsets.ViewSet):
    def contactList(self, request):
        queryset = ContactModel.objects.all()
        serializer = ContactSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class GalleryView(viewsets.ViewSet):
    def galleryImages(self, request):
        queryset = Gallery.objects.all()
        serializer = GallerySerializer(queryset, many=True)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class SubscriptionPlans(viewsets.ViewSet):
    def plan_list(self, request):
        queryset = SubscriptionPlan.objects.all()
        serializer = SubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionEditDelete(APIView):
    def get_object(self, pk):
        try:
            return SubscriptionPlan.objects.get(pk=pk)
        except SubscriptionPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        plan = self.get_object(pk)
        Plan = SubscriptionSerializer(plan)
        return Response(Plan.data)

    def put(self, request, pk, format=None):
        plan_obj = self.get_object(pk)
        serializer = SubscriptionSerializer(plan_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        plan_obj = self.get_object(pk)
        plan_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BMRCalculator(APIView):
    def get_object(self, pk):
        try:
            return UserExtension.objects.get(user=pk)
        except UserExtension.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        User = BMRCalculatorSerializer(user, context={"request": request})
        return Response(User.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = BMRCalculatorSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BMRValuesByUser(APIView):
    def get_object(self, pk):
        try:
            obj = BMRValues.objects.filter(user=pk)
            return obj
        except BMRValues.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        bmr = self.get_object(pk)
        BMR = BMRValuesSerializer(bmr, many=True, context={"request": request})
        return Response(BMR.data)


class PostBMR(viewsets.ViewSet):
    def bmr_list(self, request):
        queryset = BMRValues.objects.all()
        serializer = BMRValuesSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BMRValuesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def handle__uploaded_file(f):
    if not os.path.isdir("media/uppy_images/"):
        os.makedirs("media/uppy_images/")

    with open('media/uppy_images/'+f.name, 'wb+') as destination:
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
            res['url'] = 'http://www.mytruestrength.com/backend/media/uppy_images/' + handle__uploaded_file(self.request.FILES[i])
            array['file'] = res
        return Response(array)


class GalleryImageUpdate(APIView):
    def get_object(self, pk):
        try:
            return Gallery.objects.get(id=pk)
        except Gallery.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = GallerySerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = GallerySerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryImages(viewsets.ViewSet):
    def images(self, request):
        queryset = Gallery.objects.all()
        serializer = GallerySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class FindTrainerView(viewsets.ViewSet):
    def list(self, request):
        queryset = FindTrainer.objects.all()
        serializer = FindTrainerSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FindTrainerSerializer(data=request.data)
        account_sid = "ACa5cd6a809b1ddd9b8f111a6a9bdd9c0f"
        auth_token = "21ea5512e4f0ccb10ae519c6b8530e17"
        client = Client(account_sid, auth_token)

        client.messages.create(
            to="+91"+request.data['phone'],
            from_="+19105579284",
            body="Hii "+request.data['name'] + ', ' + 'we will find a trainer near you and contact you shortly. Join Transformers Fitness Academy today.',
            media_url="https://climacons.herokuapp.com/clear.png")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateCoupon(viewsets.ViewSet):
    def coupon_list(self, request):
        queryset = Coupon.objects.all()
        serializer = CouponSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCouponCodeByUser(APIView):
    def get_object(self, pk):
        try:
            return Coupon.objects.get(user=pk)
        except Coupon.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = CouponSerializer(obj)
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = CouponSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSubscriptionPost(viewsets.ViewSet):
    def s_list(self, request):
        queryset = UserSubscription.objects.all()
        serializer = UserSubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
