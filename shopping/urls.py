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
]