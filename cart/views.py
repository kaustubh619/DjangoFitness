from rest_framework import generics
from cart.models import Cart
from products.models import Products
from django.http import HttpResponse
from .serializers import CartCreateSerializer, CartListSerializer, CartQuantitySerializer
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from django.http import Http404


class CartCreateView(APIView):
    def post(self, request):
        serializer = CartCreateSerializer(data=request.data)
        user_id = request.data.get('customer_id')
        product_info = request.data.get('product_info')

        item_exists_in_cart = Cart.objects.filter(Q(product_info__id=product_info) & Q(customer_id__id=user_id))

        print(item_exists_in_cart.count())

        if item_exists_in_cart.count() == 0:
            # perform creation
            serializer = CartCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        else:
            # perform updation
            cart_object = Cart.objects.filter(Q(product_info__id=product_info) & Q(customer_id__id=user_id)).first()
            serializer = CartCreateSerializer(cart_object, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartListByUserView(generics.ListAPIView):
    lookup_field = 'customer_id'
    serializer_class = CartListSerializer

    def get_queryset(self):
        pk = self.kwargs.get("customer_id")
        return Cart.objects.filter(customer_id=pk)


class DeleteCartItemById(APIView):
    def get_object(self, pk):
        try:
            return Cart.objects.filter(id=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = CartCreateSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartDeleteByUser(APIView):
    def get_object(self, pk):
        try:
            return Cart.objects.filter(customer_id=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = CartCreateSerializer(obj, context={"request": request}, many=True)
        return Response(Obj.data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)