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
    path("delete_cart_item/<int:item_id>/", views.delete_cart_item, name="delete_cart_item"),    #刪除購物車內商品
    path("check_order/", views.check_order, name="check_order"),     #顯示購物車內容、計算金額、送貨資訊等
    path("checkout/", views.checkout, name="checkout"),      #↑按下結帳後，生成訂單、清空購物車內東西
    path("order/", views.order, name="order"),   #查看訂單
    path("follow_list/", views.follow_list, name="follow_list"),   #查看關注清單
    path("delete_follow_list_item/<int:item_id>/", views.delete_follow_list_item, name="delete_follow_list_item"), 
]