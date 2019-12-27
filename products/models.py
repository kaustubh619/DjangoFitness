import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save


ORDER_STATUS = ((0, 'Offline'), (1, 'Active'), (2, 'Out of Stock'))


class Categories(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100, default="Category")

    def __str__(self):
        return str(self.name)


class subCategories(models.Model):
    class Meta:
        verbose_name_plural = "Sub Categories"

    category      = models.ForeignKey(Categories, on_delete=models.CASCADE) 
    name          = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class sub_subCategories(models.Model):
    class Meta:
        verbose_name_plural = "Brands"

    category      = models.ForeignKey(subCategories, on_delete=models.CASCADE) 
    name          = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)


# Create your models here.
class Products(models.Model):
    class Meta:
        verbose_name_plural = "Products"
        managed = True

    # pk aka id --> numbers
    # user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    product_name       = models.CharField(max_length=120, null=True, blank=True )
    product_id         = models.UUIDField(null=False, blank=False, default=uuid.uuid4 )
    slug               = models.SlugField(unique=True, null=True)
    description        = models.TextField(null=True, blank=True)
    seller_id          = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)

    price              = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0)
    discount           = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0)

    images             = models.TextField(null=True, blank=True)

    specifications     = models.TextField(null=True, blank=True)
    
    bmr_min            = models.PositiveIntegerField(null=False, blank=False)
    bmr_max            = models.PositiveIntegerField(null=False, blank=False)


    category           = models.ForeignKey(Categories, null=True, on_delete=models.SET_NULL,related_name='categorys') 
    subcategory        = models.ForeignKey(subCategories, null=True, on_delete=models.SET_NULL,related_name='subCategory')
    brand              = models.ForeignKey(sub_subCategories, null=True, on_delete=models.SET_NULL,related_name='brand')

    status             = models.PositiveSmallIntegerField(choices=ORDER_STATUS, default=0)

    #timestamps
    created_date       = models.DateTimeField(auto_now_add=True)
    modified_date      = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.user.email)

    
    def __str__(self):
        return str(self.product_name)
        


    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.headline)
    #     super(Products , self).save(*args, **kwargs)
        

    # @property
    # def owner(self):
    #     return self.user

    # def get_absolute_url(self):
    #     return reverse("api-postings:post-rud", kwargs={'pk': self.pk}) '/api/postings/1/'
    
    # def get_api_url(self, request=None):
    #     return api_reverse("api-postings:post-rud", kwargs={'pk': self.pk}, request=request)


# def create_slug(instance , new_slug = None):
#      slug  = slugify(instance.product_name)
#      if new_slug is not None:
#          slug = new_slug
#      qs = 


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    slug  = slugify(instance.product_name)

    print(uuid.uuid4())

    exists = Products.objects.filter(slug=slug).exists()
    if exists:
        slug = "%s-%s" %(slug, uuid.uuid4())
    instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender = Products)