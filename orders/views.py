from django.shortcuts import render
from rest_framework import generics
from orders.models import Orders, OrderSession
from cart.models import Cart
from .serializers import OrderSessionSerializer, CreateOrderSerializer, EditOrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random
#
import environ
import razorpay
import datetime
import json
# from rest_framework.views import APIView
# from utils.helper import get_user_id
# from users.models import User, customer_address
# from products.models import seller_products, Products
# from django.db import transaction
from django.db.models import Q, F, Count, Sum
from django.shortcuts import get_object_or_404
from datetime import timedelta
from products.models import Products
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from rest_framework.views import APIView

# env = environ.Env()
#
# if env('PAYMENT_MODE') == 'Live':
#     client = razorpay.Client(auth=(env('RAZORPAY_LIVE_KEY_ID'), env('RAZORPAY_LIVE_KEY_SECRET')))
# else:
#     client = razorpay.Client(auth=(env('RAZORPAY_TEST_KEY_ID'), env('RAZORPAY_TEST_KEY_SECRET')))

client = razorpay.Client(auth=("rzp_test_9iatHS2w5hnv4n", "shTVYb3WhlaB14khnD3NwVKQ"))


class CreateOrderSession(generics.CreateAPIView):
    serializer_class = OrderSessionSerializer

    def create(self, request, *args, **kwargs):

        response = {}

        if request.POST.get("cart_keys"):

            customer_id = request.data.get('customer_id')

            string = request.POST.get("cart_keys").rstrip(',')

            cart_keys = string.replace(" ", "").split(",")

            qs = Cart.objects.filter(cart_key__in=cart_keys).values(
                'total_price',
                'quantity',
                'cart_key',
                product_id=F('product_info__product_id'),
                product_name=F('product_info__product_name'),
                product_price=F('product_info__price'),
                seller_id=F('product_info__seller_id__id'),
            )

            amount = 0

            source = request.data.get('source')

            if request.POST.get("source"):
                source = request.POST.get("source")

            # for i in qs:
            amount = request.POST.get("amount")

            if len(cart_keys) == qs.count():

                qr = OrderSession.objects.create(
                    cart_keys=json.dumps(list(qs), indent=None, sort_keys=True, default=str),
                    customer_id=customer_id,
                    amount=amount,
                    source=source
                )

                return Response({
                    'status': 200,
                    'message': 'Order Created',
                    'session_key': qr.session_key,
                    'amount': qr.amount,
                    'items': qs.count(),
                    'created': qr.created_date,
                })

            else:
                return Response({
                    'status': 409,
                    'message': 'Cart Item Conflict. Cart item count doesnt match',
                }, status=status.HTTP_409_CONFLICT)
        else:
            return Response({
                'status': 404,
                'message': 'Missing Information',
            }, status=status.HTTP_404_NOT_FOUND)


class CreateOrder(generics.CreateAPIView):
    lookup_field = 'order_id'
    serializer_class = CreateOrderSerializer
    queryset = Orders.objects.all()

    def post(self, request, format=None):

        user_id = request.POST.get('user_id')

        response_data = {}
        razorpay_amount = 0

        session_key = request.POST.get('session_key')

        session = OrderSession.objects.filter(session_key=session_key).values(
            'amount',
            'cart_keys',
            'created_date'
        )

        print(session_key)

        cart = json.loads(list(session)[0]['cart_keys'])

        for i in cart:
            razorpay_amount += float(i['total_price']) * 100

        real_amount = int(razorpay_amount / 100)

        address = request.POST.get('delivery_address')

        now = datetime.datetime.now()
        year = '{:02d}'.format(now.year)
        month = '{:02d}'.format(now.month)
        day = '{:02d}'.format(now.day)
        day_month_year = '{}{}{}'.format(year, month, day)

        seller = day_month_year + str(random.randrange(1, 10 ** 6))

        actual_amount = request.data.get("actual_amount")

        DATA = {'amount': actual_amount, 'currency': 'INR', 'receipt': seller, 'payment_capture': 1}

        val = {}

        if request.POST.get('payment_method') is not '4':
            val = client.order.create(data=DATA)
        else:
            val['id'] = ""
            val['receipt'] = day_month_year + str(random.randrange(1, 10 ** 6))
            val['attempts'] = '1'

        print(val)

        response_data['real_amount'] = real_amount
        response_data['razorpay_amount'] = razorpay_amount

        if True:
            for i in cart:
                response_data['message'] = 'success'
                response_data['status'] = '200'
                response_data['invoice_id'] = day_month_year + str(random.randrange(1, 10 ** 6))
                response_data['order_id'] = val['id']
                response_data['status'] = 'CREATED'
                response_data['receipt'] = val['receipt']
                response_data['attempts'] = val['attempts']
                response_data['info'] = val

                Orders.objects.create(
                    order_id=seller,
                    delivery_address=request.data.get('delivery_address'),
                    # json.dumps(list(getAddress), indent=None, sort_keys=True, default=str)
                    payment_method=request.POST.get('payment_method'),
                    payment_detail=request.POST.get('payment_detail'),
                    razor_order_id=response_data['order_id'],
                    invoice_id=response_data['invoice_id'],
                    customer=User.objects.get(id=user_id),
                    product_id=Products.objects.get(product_id=i['product_id']),
                    product_name=i['product_name'],
                    is_multiple=True,
                    product_price=i['total_price'],
                    source='MyTrueStrength',
                    session_key=OrderSession.objects.get(session_key=session_key),
                )
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data['status'] = 401
            response_data['message'] = "Order Session Expired. Please move to Cart"
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        response_data['status'] = 404
        response_data['message'] = "Order Session Invalid"
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class GetOrderSession(generics.ListAPIView):
    def get_object(self, session_key):
        try:
            return OrderSession.objects.get(session_key=session_key)
        except OrderSession.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        blog = self.get_object(slug)
        Blog = OrderSessionSerializer(blog, context={"request": request})
        return Response(Blog.data)


class EditOrderByRazorPayOrderID(APIView):
    def get_object(self, razor_order_id):
        try:
            return Orders.objects.filter(razor_order_id=razor_order_id)
        except Orders.DoesNotExist:
            raise Http404

    def get(self, request, razor_order_id):
        obj = self.get_object(razor_order_id)
        Obj = EditOrderSerializer(obj, many=True)
        return Response(Obj.data)

    def put(self, request, razor_order_id):
        obj = self.get_object(razor_order_id)

        for i in obj:
            print(i)
            serializer = EditOrderSerializer(i, data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
        return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderSessionDeleteByUser(APIView):
    def get_object(self, session_key):
        try:
            return OrderSession.objects.filter(session_key=session_key)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, session_key):
        obj = self.get_object(session_key)
        Obj = OrderSessionSerializer(obj, context={"request": request}, many=True)
        return Response(Obj.data)

    def delete(self, request, session_key):
        obj = self.get_object(session_key)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
