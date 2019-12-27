from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


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
