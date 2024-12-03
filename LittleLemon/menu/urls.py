from django.urls import path
from .views import MenuItemList, MenuItemDetail

urlpatterns = [
    path('menu-items/', MenuItemList.as_view(), name='menu-items-list'),
    path('menu-items/<int:pk>/', MenuItemDetail.as_view(), name='menu-items-detail'),
]
