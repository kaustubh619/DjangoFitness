from django.urls import path
from . import views

urlpatterns = [
    path('api/login', views.login_admin),
    path('api/login/customer', views.login_customer),
    path('api/register', views.register),
    path('user', views.UserListView.as_view({'get': 'userList'})),
    path('user/<int:pk>', views.UserUpdateDetail.as_view()),
    path('user_ext/<int:pk>', views.UserExt.as_view()),
    path('user_type_post', views.UserTypePostView.as_view({'get': 'user_type_list'})),
    path('user_ext_post', views.UserExtensionPostView.as_view({'get': 'user_extension_list'})),
    path('user_type_list', views.UserTypeListView.as_view({'get': 'userTypeList'})),
    path('user_ext', views.UserExtensionListView.as_view({'get': 'userExtList'})),
    path('user_trainer', views.TrainerListView.as_view({'get': 'userTrainerList'})),
    path('user_cust', views.CustomerListView.as_view({'get': 'userCustomerList'})),
    path('carousel_image', views.ImageView.as_view(), name="image"),
    path('contact', views.ContactListView.as_view({'get': 'contactList'})),
    path('gallery', views.GalleryView.as_view({'get': 'galleryImages'})),
    path('subscription_plan', views.SubscriptionPlans.as_view({'get': 'plan_list'})),
    path('sub_plan/<int:pk>', views.SubscriptionEditDelete.as_view()),
    path('bmr_calculator/<int:pk>', views.BMRCalculator.as_view()),
    path('bmr_values/<int:pk>', views.BMRValuesByUser.as_view()),
    path('post_bmr', views.PostBMR.as_view({'get': 'bmr_list'})),
    path('uppy_image', views.ProductUploadImage.as_view()),
    path('images_gallery', views.GalleryImages.as_view({'get': 'images'})),
    path('update_gallery/<int:pk>', views.GalleryImageUpdate.as_view()),
    path('find_trainer', views.FindTrainerView.as_view({'get': 'list'})),
]