from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from core.decorators import login_required_w_message


def home(request):
    records = Record.objects.all().order_by('pk')

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
        return render(request, 'website/home.html', {'records': records})


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
def customer_record(request, pk):
    customer_record = Record.objects.get(id=pk)
    return render(request, 'website/record.html', {'customer_record': customer_record})

@login_required_w_message()
def delete_record(request, pk):
    record_to_delete = Record.objects.get(id=pk)
    record_to_delete.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('website:home')

@login_required_w_message()
def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Record added successfully')
            return redirect('website:add_record')
        
        else:
            messages.error(request, 'Form is not valid. Check your inputs')
        
    return render(request, 'website/add_record.html', {'form': form})

@login_required_w_message()
def update_record(request, pk):
    record_to_edit = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=record_to_edit)

    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f'Record #{record_to_edit.pk} edited successfully')
            return redirect('website:home')
        
        else:
            messages.error(request, 'Error during editing. Check your form')
        
    return render(request, 'website/update_record.html', {'form': form})
    