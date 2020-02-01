from . import views
from django.urls import path

urlpatterns = [
      path('create_cart', views.CartCreateView.as_view(), name="createProduct"),
      path('cartbyuser/<int:customer_id>', views.CartListByUserView.as_view(), name="cartListByUserView"),
      path('cart_item_delete/<int:pk>', views.DeleteCartItemById.as_view()),
      path('delete_cart_items/<int:pk>', views.CartDeleteByUser.as_view()),

]