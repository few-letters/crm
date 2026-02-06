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
    path('products/', views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('orders/', views.order_list, name='order_list'),
    path('add_order/', views.add_order, name='add_order'),
    path('order/<int:pk>', views.order_detail, name='order_detail'),
    path('order/<int:pk>/update/', views.update_order, name='update_order'),
    path('order/<int:pk>/delete/', views.delete_order, name='delete_order'),
    path('master_form/', views.master_form, name='master_form'),
    #path('login/', views.login_user, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)