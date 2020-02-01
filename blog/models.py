from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from django.db.models.signals import pre_save


class BlogCategory(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name


class BlogPost(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    content = models.TextField()
    blog_img = models.ImageField(null=True, blank=True, upload_to='blog_images')
    posted_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instance.slug = slug


pre_save.connect(pre_save_post_receiver, sender=BlogPost)


class BlogComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    blog = models.ForeignKey(BlogPost, related_name='blog_comments', on_delete=models.PROTECT)
    comment = models.TextField()

    def __str__(self):
        return str(self.blog)
