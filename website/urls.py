from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('customer/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('update_customer/<int:pk>/', views.update_customer, name='update_customer'),
    path('delete/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('add_customer/', views.add_customer, name='add_customer'),
    #path('login/', views.login_user, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)