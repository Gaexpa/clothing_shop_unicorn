from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('index/category/<str:category>', views.category_search, name='category'),
    path('index/details/<int:id>', views.details, name='details'),
]