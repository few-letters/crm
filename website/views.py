from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddCustomerForm, ProductForm
from .models import Customer, Order, Product
from core.decorators import login_required_w_message
from django.db.models import Q


def home(request):
    customers = Customer.objects.all().order_by('-updated_at')
    search_query = request.GET.get('q')
        
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
    )

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
        return render(request, 'website/home.html', {'customers': customers})


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
        
    return render(request, 'website/product_list.html', {'products': products})


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
def delete_customer(request, pk):
    customer_to_delete = Customer.objects.get(id=pk)
    customer_to_delete.delete()
    messages.success(request, 'Customer deleted successfully')
    return redirect('website:home')


@login_required_w_message()
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    
    if request.method == 'POST':
        product.delete() # Hard delete, можна потім ще is_active=false 
        messages.success(request, "Product deleted successfully")
        return redirect('website:product_list')
        
    return redirect('website:product_list')