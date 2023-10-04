from django.urls import path
from .  import views

urlpatterns=[
    path('', views.login, name='login'),
    path('home/',views.home,name='home'),
    path('eT_Invoice/',views.eT_Invoice,name='eT_Invoice'),
    path('Salary_Slip/',views.Salary_Slip,name='Salary_Slip'),
    path('Client_Invoice/',views.Client_Invoice,name='Client_Invoice'),
    path('logout/', views.logout, name='logout'),
]