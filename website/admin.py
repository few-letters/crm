from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, Order, OrderItem, Product

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ['product']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('product')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'created_at', 'get_total_cost')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
    list_select_related = ['customer']

    def get_total_cost(self, obj,):
        return obj.get_total_cost()
    get_total_cost.short_description = 'Total Cost'