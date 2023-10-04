from django.shortcuts import render,redirect
from .decorators import login_admin_successfull
from django.views.decorators.cache import cache_control

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'eSparkAdmin' and password == 'admin@espark':
            request.session['role'] = 'admin'
            return redirect("home")

        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    response = render(request, 'login.html')
    # Add Cache-Control header to prevent caching
    response['Cache-Control'] = 'no-store, must-revalidate'

    return response

@login_admin_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    return render(request,'home.html')

@login_admin_successfull
def eT_Invoice(request):
    return render(request,'eT_Invoice.html')

@login_admin_successfull
def Salary_Slip(request):
    return render(request,'Salary_Slip.html')

@login_admin_successfull
def Client_Invoice(request):
    return render(request,'Client_Invoice.html')

def logout(request):
    if 'role' in request.session:
        del request.session['role']
    
    return redirect('login')