from django.db import models
from products.models import Products
from django.contrib.auth.models import User
import random
from django.db.models.signals import pre_save


class Cart(models.Model):
    cart_key = models.CharField(max_length=100, null=True)
    product_info = models.ForeignKey(Products, null=False, on_delete=models.DO_NOTHING)
    customer_id = models.ForeignKey(User, null=False, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0)
    single_item_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cart_key)


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if instance._state.adding:
        cart_key = "CA" + str(random.randrange(1, 10 ** 10))
        print('this is an adding')
        instance.cart_key = cart_key


pre_save.connect(pre_save_post_receiver, sender=Cart)
