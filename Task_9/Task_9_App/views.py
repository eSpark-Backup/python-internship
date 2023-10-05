from django.shortcuts import render,redirect
from .decorators import login_admin_successfull
from django.views.decorators.cache import cache_control
from . models import eT_Invoice

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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def eT_Invoice(request):
    if request.method=='POST':
        attention=request.POST['attention']
        company_name=request.POST['comp_name']
        email=request.POST['email']
        company_address=request.POST['comp_addr']
        date=request.POST['date']
        month=request.POST['inv_month']
        emp_id=request.POST['emp_id']
        emp_name=request.POST['emp_name']
        emp_desig=request.POST['emp_desig']
        proj_name=request.POST['proj_name']
        job_mode=request.POST['job_mode']
        join_date=request.POST['join_date']
        ser_char_hours = int(request.POST['ser_char_hours'])
        ser_char_per_hour = int(request.POST['ser_char_per_hour'])
        man_char_hours = int(request.POST['man_char_hours'])
        man_char_per_hour = int(request.POST['man_char_per_hour'])

        ser_char_amount = ser_char_hours*ser_char_per_hour
        man_char_amount = man_char_hours*man_char_per_hour

        total = 'Rs '+str(ser_char_amount+man_char_amount)

        emp_info={
            'emp_id':emp_id,
            'emp_name':emp_name,
            'emp_desig':emp_desig,
            'proj_name':proj_name,
            'job_mode':job_mode
        }

        sal_info={
            'service_charges':[ser_char_hours,ser_char_per_hour,ser_char_amount],
            'management_fees:':[man_char_hours,man_char_per_hour,man_char_amount]
        }

        # new_invoice_eT = eT_Invoice.objects.create(attention=attention, company_name=company_name, email=email, company_address=company_address, date=date, month=month, emp_info=emp_info, sal_info=sal_info)

        current_invoice_number = 'ES-2023-000000'

        return render(request, 'eT_Invoice_pdf.html', {
            'current_invoice_number' : current_invoice_number,
            'attention' : attention,
            'company_name' : company_name,
            'email' : email,
            'company_address' : company_address,
            'date' : date,
            'month' : month,
            'emp_id' : emp_id,
            'emp_name' : emp_name,
            'emp_desig':emp_desig,
            'proj_name' : proj_name,
            'job_mode' : job_mode,
            'join_date' : join_date,
            'ser_char_hours' : ser_char_hours,
            'ser_char_per_hour' : ser_char_per_hour,
            'man_char_hours' : man_char_hours,
            'man_char_per_hour' : man_char_per_hour,
            'ser_char_amount' : ser_char_amount,
            'man_char_amount' : man_char_amount,
            'total' : total
        })

    return render(request,'eT_Invoice.html')

@login_admin_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Salary_Slip(request):
    return render(request,'Salary_Slip.html')

@login_admin_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Client_Invoice(request):
    return render(request,'Client_Invoice.html')

def logout(request):
    if 'role' in request.session:
        del request.session['role']
    
    return redirect('login')