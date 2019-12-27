from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('api/login', views.login_admin),
    path('api/login/customer', views.login_customer),
    path('api/register', views.register),
    url(r'^user$', views.UserListView.as_view({'get': 'userList'})),
    url(r'^user/(?P<pk>[0-9]+)$', views.UserUpdateDetail.as_view()),
    url(r'^user_ext/(?P<pk>[0-9]+)$', views.UserExt.as_view()),
    url(r'^user_type_post$', views.UserTypePostView.as_view({'get': 'user_type_list'})),
    url(r'^user_ext_post$', views.UserExtensionPostView.as_view({'get': 'user_extension_list'})),
    url(r'^user_type_list$', views.UserTypeListView.as_view({'get': 'userTypeList'})),
    url(r'^user_ext$', views.UserExtensionListView.as_view({'get': 'userExtList'})),
    url(r'^user_trainer$', views.TrainerListView.as_view({'get': 'userTrainerList'})),
    url(r'^user_cust$', views.CustomerListView.as_view({'get': 'userCustomerList'})),
    # path('carousel_image', views.CarouselImageUploadView.as_view()),
    path('carousel_image', views.ImageView.as_view(), name="image"),
    url(r'^contact', views.ContactListView.as_view({'get': 'contactList'})),
    url(r'^gallery', views.GalleryView.as_view({'get': 'galleryImages'})),
    url(r'^subscription_plan$', views.SubscriptionPlans.as_view({'get': 'plan_list'})),
    url(r'^sub_plan/(?P<pk>[0-9]+)$', views.SubscriptionEditDelete.as_view()),
    url(r'^bmr_calculator/(?P<pk>[0-9]+)$', views.BMRCalculator.as_view()),
    url(r'^bmr_values/(?P<pk>[0-9]+)$', views.BMRValuesByUser.as_view()),
    url(r'^post_bmr$', views.PostBMR.as_view({'get': 'bmr_list'})),
]
