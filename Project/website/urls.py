from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('restaurant/menu_list/<int:menu_item_id>/', views.menu_item, name='menuitem'),
    path('restaurant/menu_list/', views.menu_list, name='menulist'),
    path('restaurant/<int:restaurant_id>/', views.restaurant, name='restaurant'),
    path('restaurant/', views.restaurant_list, name='restaurants')
]
