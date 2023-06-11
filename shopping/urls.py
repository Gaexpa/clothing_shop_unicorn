from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("index/category/<str:category>", views.category_search, name="category"),
    path("index/details/<int:id>", views.details, name="details"),
    path("cart/", views.view_cart, name="cart"),
    path("delete/<int:item_id>/", views.delete_item, name="delete_item"),
    path("checkout/", views.checkout, name="checkout"),
    path("check_order/", views.check_order, name="check_order"),
]
