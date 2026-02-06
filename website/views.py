from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddCustomerForm, ProductForm, OrderForm, OrderItemFormSet
from .models import Customer, Order, Product
from core.decorators import login_required_w_message
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator


def home(request):
    customers = Customer.objects.all().order_by('-updated_at')
    search_query = request.GET.get('q')
        
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
    )
        
    paginator = Paginator(customers, 8)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('website:home')
        else:
                messages.error(request, 'Something went wrong, try again.')
                return redirect('website:home')

    else:
        return render(request, 'website/home.html', {'customers_page': page_obj})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('website:home')


def register_user(request):
    form = SignUpForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registered successfully')
            return redirect('website:home')
        
        else:
             messages.error(request, 'Form is not valid. Check your inputs')
    
    return render(request, 'website/register.html', {'form': form})


@login_required_w_message()
def customer_detail(request, pk):
    customer = Customer.objects.get(id=pk)
    return render(request, 'website/customer_detail.html', {'customer': customer})


@login_required_w_message()
def delete_customer(request, pk):
    customer_to_delete = Customer.objects.get(id=pk)
    customer_to_delete.delete()
    messages.success(request, 'Customer deleted successfully')
    return redirect('website:home')


@login_required_w_message()
def add_customer(request):
    form = AddCustomerForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully')
            return redirect('website:add_customer')
        
        else:
            messages.error(request, 'Form is not valid. Check your inputs')
        
    return render(request, 'website/add_customer.html', {'form': form})


@login_required_w_message()
def update_customer(request, pk):
    customer_to_update = Customer.objects.get(id=pk)
    form = AddCustomerForm(request.POST or None, instance=customer_to_update)

    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f'Customer #{customer_to_update.pk} edited successfully')
            return redirect('website:home')
        
        else:
            messages.error(request, 'Error during editing. Check your form')
        
    return render(request, 'website/update_customer.html', {'form': form})
    

@login_required_w_message()
def product_list(request):
    products = Product.objects.all().order_by('-updated_at')
    search_query = request.GET.get('q')
        
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)  #Не оптимально для highload. Потім почитати про SearchVector
    )
        
    paginator = Paginator(products, 4)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
        
    return render(request, 'website/product_list.html', {'products_page': page_obj})


@login_required_w_message()
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully")
            return redirect('website:product_list')
        else:
            messages.error(request, "Please correct the errors in form")
    else:
        form = ProductForm()

    return render(request, 'website/add_product.html', {'form': form})


@login_required_w_message()
def product_detail(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully")
            return redirect('website:product_list')
        else:
            messages.error(request, "Please correct the errors in form")

    else:
        form=ProductForm(instance=product)

    return render(request, 'website/product_detail.html', {'product': product, 'form': form})


@login_required_w_message()
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    
    if request.method == 'POST':
        product.delete() # Hard delete, можна потім ще is_active=false 
        messages.success(request, "Product deleted successfully")
        return redirect('website:product_list')
        
    return redirect('website:product_list')


@login_required_w_message()
def order_list(request):
    orders = Order.objects.select_related('customer').all().order_by('-updated_at')
    search_query = request.GET.get('q')
    
    if search_query:
        orders = orders.filter(
            Q(id__icontains=search_query) | 
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(customer__email__icontains=search_query) |
            Q(customer__id__icontains=search_query)
        )

    paginator = Paginator(orders, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'website/order_list.html', {'orders_page': page_obj})


@login_required_w_message()
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():            
            try:
                with transaction.atomic():
                    order = form.save()
                    formset.instance = order
                    formset.save()
                    
                messages.success(request, 'Order created successfully!')
                return redirect('website:order_list')
                
            except Exception as e:
                messages.error(request, f"Error creating order: {e}")
        else:
            messages.error(request, "Please correct the errors in form")
            
    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'website/add_order.html', {'form': form, 'formset': formset})


@login_required_w_message()
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related('customer').prefetch_related('items__product'),
        id=pk
    )
    return render(request, 'website/order_detail.html', {'order': order})


@login_required_w_message()
def update_order(request, pk):
    order = get_object_or_404(Order.objects.select_related('customer'), id=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    formset.save()

                    messages.success(request, 'Order updated successfully')
                    return redirect('website:order_detail', pk=order.id)
                
            except Exception as e:
                messages.error(request, 'Error: {e}')

        else:
            messages.error(request, 'Check errors in form')
        
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
        
    return render(request, 'website/update_order.html', {
        'form': form,
        'formset': formset,
        'order': order
    })          


@login_required_w_message()
def delete_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    
    if request.method == 'POST':
        order.delete()
        messages.success(request, f"Order #{pk} deleted successfully")
        return redirect('website:order_list')
    
    return redirect('website:order_list')


@login_required_w_message()
def master_form(request):
    if request.method == 'POST':
        customer_form = AddCustomerForm(request.POST, prefix='customer')
        order_form = OrderForm(request.POST, prefix='order')
        formset = OrderItemFormSet(request.POST, prefix='items')    # по дефолту стояв би і так 'items', бо в моделі related_name='items', але робимо explicitly                                    
        del order_form.fields['customer'] # щоб пройти валідацію не передавши користувача (він ще не створений)

        if customer_form.is_valid() and order_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    customer = customer_form.save()
                    order = order_form.save(commit=False)
                    order.customer = customer
                    order.save()

                    formset.instance = order
                    formset.save()
                    messages.success(request, f'Customer #{customer.id} and Order #{order.id} created successfully')
                    return redirect('website:order_detail', pk=order.id)

            except Exception as e:
                messages.error(request, 'Error: {e}')
        
        else:
            messages.error(request, 'Check errors in form')
    
    else:
        customer_form = AddCustomerForm(prefix='customer')
        order_form = OrderForm(prefix='order')
        formset = OrderItemFormSet(prefix='items')

    return render(request, 'website/master_form.html', {
        'customer_form': customer_form,
        'order_form': order_form,
        'formset': formset
    })