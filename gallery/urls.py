from django.urls import path
from .views import OrderCreateView, OrderListView, painting_list_api

urlpatterns = [
    path("api/orders/create/", OrderCreateView.as_view(), name="create_order"),
    path("api/orders/list/", OrderListView.as_view(), name="order_list"),
    path("api/paintings/", painting_list_api, name="painting_list_api"),
]

