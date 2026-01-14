from django.urls import path, include
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>/', views.customer_record, name='record'),
    path('update_record/<int:pk>/', views.update_record, name='update_record'),
    path('delete/<int:pk>/', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    #path('login/', views.login_user, name='login'),
]