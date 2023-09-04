from django.urls import path
from .  import views

urlpatterns=[
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('result_item/',views.result_item,name='result_item'),
    path('result_part/',views.result_part,name='result_part'),
]