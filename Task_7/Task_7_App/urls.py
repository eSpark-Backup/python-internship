from django.urls import path
from .  import views

urlpatterns=[
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('admin_home/', views.home_admin, name='home_admin'),
    path('update/', views.update_stock, name='update'),
    path('result_item/',views.result_item,name='result_item'),
    path('result_part/',views.result_part,name='result_part'),
    path('admin_result_item/',views.admin_result_item,name='admin_result_item'),
    path('admin_result_part/',views.admin_result_part,name='admin_result_part'),
    path('logout/', views.logout, name='logout'),
]