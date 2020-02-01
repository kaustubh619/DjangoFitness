import uuid
from django.db import models
from products.models import Products
from django.contrib.auth.models import User

ORDER_STATUS = ((0, 'Started'), (1, 'Placed'), (1, 'Delivered'), (2, 'Cancelled By Seller'), (3, 'Cancelled By Buyer'))

PAYMENT_STATUS = ((0, 'Pending'), (1, 'Success'), (2, 'Cancelled By Seller'), (3, 'Cancelled By Buyer'))

ORDER_SESSION_STATUS = ((0, 'Started'), (1, 'Completed'), (2, 'Cancelled'))


class OrderSession(models.Model):
    class Meta:
        verbose_name_plural = "Order Session"

    session_key = models.UUIDField(max_length=100, unique=True, null=False, default=uuid.uuid4, help_text="Auto generated")
    cart_keys = models.TextField(null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="CustomerSession")
    status = models.PositiveSmallIntegerField(choices=ORDER_SESSION_STATUS, default=0)
    source = models.CharField(max_length=100, null=True, default="Postman")

    # timestamps
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class Orders(models.Model):
    class Meta:
        verbose_name_plural = "Orders"

    order_id = models.CharField(max_length=100, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razor_order_id = models.CharField(max_length=100, null=True)
    invoice_id = models.CharField(max_length=100, null=True)
    payment_method = models.CharField(max_length=100, null=True)
    payment_detail = models.CharField(max_length=100, null=True)
    payment_status = models.PositiveSmallIntegerField(choices=PAYMENT_STATUS, default=0)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="Customer")

    # product data
    product_id = models.ForeignKey(Products, on_delete=models.DO_NOTHING, null=True)
    is_multiple = models.BooleanField(default=False)
    product_name = models.CharField(max_length=100, null=True)
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_status = models.PositiveSmallIntegerField(choices=ORDER_STATUS, default=0)
    source = models.CharField(max_length=100, null=True, default="Postman")
    delivery_address = models.TextField(null=False)
    session_key = models.ForeignKey(OrderSession, to_field="session_key", db_column="OrderSession",
                                    on_delete=models.DO_NOTHING, null=True, blank=True)

    # timestamps
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
