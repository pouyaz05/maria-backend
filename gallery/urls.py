from django.urls import path
from .views import OrderCreateView, OrderListView, painting_list_api

urlpatterns = [
    path("orders/create/", OrderCreateView.as_view(), name="create_order"),
    path("orders/list/", OrderListView.as_view(), name="order_list"),
    path("paintings/", painting_list_api, name="painting_list_api"),
]

