from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import random
from django.db.models.signals import pre_save


class UserType(models.Model):
    user_type = models.CharField(max_length=20)

    def __str__(self):
        return str(self.user_type)


class UserExtension(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserType, on_delete=models.PROTECT)
    location = models.CharField(max_length=20)
    Gender_Choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=Gender_Choices)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    bmr_value = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.user)


class Carousel(models.Model):
    img = models.ImageField(null=True, blank=True, upload_to='images')

    def __str__(self):
        return "Image " + str(self.id)


class ContactModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.IntegerField()
    enquiry = models.TextField()

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Contact'


class Gallery(models.Model):
    gallery_images = models.TextField()

    def __str__(self):
        return 'Gallery Images'


class SubscriptionPlan(models.Model):
    title = models.CharField(max_length=100)
    min_BMR_male = models.IntegerField()
    max_BMR_male = models.IntegerField()
    min_BMR_female = models.IntegerField(blank=True, null=True)
    max_BMR_female = models.IntegerField(blank=True, null=True)
    plan_features = models.TextField()
    discount_on_products = models.IntegerField()
    cost = models.IntegerField()

    def __str__(self):
        return str(self.title)


class BMRValues(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bmr_value = models.IntegerField()
    date_time = models.DateField(default=datetime.now)

    def __str__(self):
        return str(self.user) + ' ' + str(self.date_time)


class FindTrainer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin = models.IntegerField()

    def __str__(self):
        return str(self.name) + ' - ' + str(self.phone)


class Coupon(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    coupon_code = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    coupon_discount_value = models.IntegerField()

    def __str__(self):
        return str(self.user) + " " + str(self.coupon_code)


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if instance._state.adding:
        coupon_code = "TFA" + str(random.randrange(1, 10 ** 8))
        print('this is an adding')
        instance.coupon_code = coupon_code


pre_save.connect(pre_save_post_receiver, sender=Coupon)