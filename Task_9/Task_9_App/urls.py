from django.urls import path
from .  import views

urlpatterns=[
    path('', views.login, name='login'),
    path('home/',views.home,name='home'),    
    path('query_eT_Invoice/',views.search_eT_Invoice,name='query_eT_Invoice'),
    path('query_Client_Invoice/',views.search_Client_Invoice,name='query_Client_Invoice'),
    path('query_Salary_Slip/',views.search_Salary_Slip,name='query_Salary_Slip'),
    path('eT_Invoice/',views.eT_Invoice,name='eT_Invoice'),
    path('Salary_Slip/',views.Salary_Slip,name='Salary_Slip'),
    path('Client_Invoice/',views.Client_Invoice,name='Client_Invoice'),
    path('logout/', views.logout, name='logout'),
]