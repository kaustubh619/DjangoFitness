from django.contrib import admin
from .models import UserType, UserExtension, Carousel, ContactModel, Gallery, SubscriptionPlan, BMRValues

admin.site.register(UserType)
admin.site.register(UserExtension)
admin.site.register(Carousel)
admin.site.register(ContactModel)
admin.site.register(Gallery)
admin.site.register(SubscriptionPlan)
admin.site.register(BMRValues)
