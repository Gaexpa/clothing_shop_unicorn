from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register/test', views.psychometric_test, name='psychometric_test'),
    path('register/result', views.result, name='result'),
    path('index/category/<str:category>', views.category_search, name='category'),
    path('index/details/<int:id>', views.details, name='details'),
    path('search/', views.search, name='search'),

    path("cart/", views.view_cart, name="cart"),   #查看購物車
    path("delete/<int:item_id>/", views.delete_item, name="delete_item"),    #刪除購物車內商品
    path("check_order/", views.check_order, name="check_order"),     #在購物車內點結帳後，顯示
    path("checkout/", views.checkout, name="checkout"),      #
    path("order/", views.order, name="order"),
]