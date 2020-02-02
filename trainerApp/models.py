from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid
from django.contrib.auth.models import User


class TrainerBio(models.Model):
    trainer_name = models.CharField(max_length=200)
    trainer_bio = models.TextField()
    trainer_gallery = models.TextField(blank=True, null=True)
    trainer_facebook_link = models.URLField(blank=True, null=True)
    trainer_instagram_link = models.URLField(blank=True, null=True)
    trainer_linkedin_link = models.URLField(blank=True, null=True)
    trainer_contact = models.BigIntegerField()
    trainer_address = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.trainer_name


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if instance._state.adding:
        slug_extension = str(uuid.uuid4()).split("-")[0]
        slug = slugify(instance.trainer_name) + slug_extension
        instance.slug = slug


pre_save.connect(pre_save_post_receiver, sender=TrainerBio)


class TrainerRatingsAndReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trainer = models.ForeignKey(TrainerBio, on_delete=models.CASCADE)
    ratings = models.IntegerField(default=0)
    reviews = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.trainer)
