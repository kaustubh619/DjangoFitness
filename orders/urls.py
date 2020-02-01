from django.urls import path
from . import views

urlpatterns = [
    path('create_order_session', views.CreateOrderSession.as_view(), name="CreateOrderSession"),
    path('create_order', views.CreateOrder.as_view(), name="CreateOrder"),
    path('get_order_session/<slug:slug>', views.GetOrderSession.as_view()),
    path('edit_order/<slug:razor_order_id>', views.EditOrderByRazorPayOrderID.as_view()),
    path('delete_order_session/<slug:session_key>', views.OrderSessionDeleteByUser.as_view()),
]
