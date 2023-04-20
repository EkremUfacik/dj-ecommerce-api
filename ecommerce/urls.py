from django.urls import path
from rest_framework.routers import DefaultRouter 

from .views import (
    ItemMVS,
    OrderItemMVS,
    OrderListView,
    OrderCreateView,
    OrderDetailView,
    AddressMVS,
)

router = DefaultRouter()
router.register("items",ItemMVS)
router.register("orderitems",OrderItemMVS)
router.register("address",AddressMVS)


urlpatterns = [
    path("orders-list/", OrderListView.as_view()),
    path("order-create/", OrderCreateView.as_view()),
    path("order-details/<int:pk>/", OrderDetailView.as_view()),
]

urlpatterns += router.urls