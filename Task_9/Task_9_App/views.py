from django.shortcuts import render,redirect
from .decorators import login_admin_successfull
from django.views.decorators.cache import cache_control
from . models import eT_Invoice_Table,Salary_Slip_Table,Client_Invoice_Table

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
        services = [service for service in request.POST.getlist('services[]') if service]
        hours = [hour for hour in request.POST.getlist('hours[]') if hour]
        hourly_rates = [rate for rate in request.POST.getlist('hourly_rate[]') if rate]

        emp_info={
            'emp_id':emp_id,
            'emp_name':emp_name,
            'emp_desig':emp_desig,
            'proj_name':proj_name,
            'job_mode':job_mode,
            'join_date':join_date
        }

        sal_info = {
            'services': services,
            'hours': [int(hour) for hour in hours],
            'hourly_rates': [int(rate) for rate in hourly_rates],
            'amounts': [int(hour) * int(rate) for hour, rate in zip(hours, hourly_rates)]
        }

        total = sum(sal_info['amounts'])

        new_invoice_eT = eT_Invoice_Table.objects.create(attention=attention, company_name=company_name, email=email, company_address=company_address, date=date, month=month, emp_info=emp_info, sal_info=sal_info)

        current_invoice_number = new_invoice_eT.invoice_no

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
            'sal_info' : sal_info,
            'total' : total
        })

    return render(request,'eT_Invoice.html')

@login_admin_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Salary_Slip(request):
    if request.method=='POST':
        emp_id=request.POST['emp_id']
        emp_name=request.POST['emp_name']
        desig=request.POST['desig']
        tot_ser=request.POST['tot_serv']
        join_date=request.POST['join_date']
        payroll_month=request.POST['payroll_month']
        status=request.POST['status']
        email=request.POST['email']
        phone_no=request.POST['phone_no']
        bank_acc=request.POST['bank_acc']
        nok=request.POST['nok']
        earnings = [earning for earning in request.POST.getlist('earning[]') if earning]
        earn_amount = [int(amount) for amount in request.POST.getlist('earn_amount[]') if amount]
        deductions = [deduction if deduction else '-' for deduction in request.POST.getlist('deduction[]')]
        deduct_amount = [int(amount) for amount in request.POST.getlist('deduct_amount[]') if amount]
        total_earn = sum(earn_amount)
        
        total_deduc = sum(deduct_amount)

        sal_info={
            'Earning_Description' : earnings,
            'Earn_Amount' : earn_amount,
            'Deduction_Recoveries' : deductions,
            'Deduct_Amount' : deduct_amount
        }

        net_pay= total_earn - total_deduc

        new_sal_slip=Salary_Slip_Table.objects.create(emp_id=emp_id,emp_name=emp_name,desig=desig,tot_ser=tot_ser,join_date=join_date,payroll_month=payroll_month,status=status,email=email,phone_no=phone_no,bank_acc=bank_acc,nok=nok,sal_info=sal_info)

        return render(request,'Salary_Slip_pdf.html',{
            "emp_id":emp_id,
            "emp_name":emp_name,
            "desig":desig,
            "tot_ser":tot_ser,
            "join_date":join_date,
            "payroll_month":payroll_month,
            "status":status,
            "email":email,
            "phone_no":phone_no,
            "bank_acc":bank_acc,
            "nok":nok,
            "sal_info":sal_info,
            "total_earn": total_earn,
            "total_deduct": total_deduc,
            "net_pay": net_pay
         })


    return render(request,'Salary_Slip.html')

@login_admin_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Client_Invoice(request):
    if request.method=='POST':
        inv_recipient=request.POST["inv_recipient"]
        attention=request.POST["attention"]
        prep_by=request.POST["prep_by"]
        date=request.POST["date"]
        contact_per=request.POST["contact_per"]
        email=request.POST["email"]
        items=[item for item in request.POST.getlist('item[]') if item]
        specs=[spec for spec in request.POST.getlist('specs[]') if spec]
        qtys=[int(qty) for qty in request.POST.getlist('qty[]') if qty]
        prices=[int(price) for price in request.POST.getlist('price[]') if price]

        amounts=[]
        for i in range(len(qtys)):
            amounts.append(qtys[i]*prices[i])

        total=sum(amounts)

        item_desc={
            'items':items,
            'specs': specs,
            'qtys':qtys,
            'prices':prices,
            'amounts':amounts
        }

        new_client_invoice=Client_Invoice_Table.objects.create(inv_recipient=inv_recipient,attention=attention,prep_by=prep_by,date=date,contact_per=contact_per,email=email,item_desc=item_desc)

        new_inv_no=new_client_invoice.invoice_no

        return render(request, 'Client_Invoice_pdf.html', {
            "inv_recipient":inv_recipient,
            "attention":attention,
            "invoice_no":new_inv_no,
            "prep_by":prep_by,
            "date":date,
            "contact_per":contact_per,
            "email":email,
            "item_desc": item_desc,
            "total":total
        })

    return render(request,'Client_Invoice.html')

@login_admin_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_eT_Invoice(request):
    if request.method=='POST':
        inv_no=request.POST['inv_no']

        try:
            invoice_data = eT_Invoice_Table.objects.get(invoice_no=inv_no)
        except ETInvoice.DoesNotExist:
            invoice_data = None


        if invoice_data!=None:
            attention=invoice_data.attention
            company_name=invoice_data.company_name
            email=invoice_data.email
            company_address=invoice_data.company_address
            date=invoice_data.date
            month=invoice_data.month
            emp_info=invoice_data.emp_info
            sal_info=invoice_data.sal_info
            total = sum(sal_info['amounts'])
            
            return render(request, 'eT_Invoice_pdf.html', {
            'current_invoice_number' : inv_no,
            'attention' : attention,
            'company_name' : company_name,
            'email' : email,
            'company_address' : company_address,
            'date' : date,
            'month' : month,
            'emp_id' : emp_info['emp_id'],
            'emp_name' : emp_info['emp_name'],
            'emp_desig':['emp_desig'],
            'proj_name' : ['proj_name'],
            'job_mode' : ['job_mode'],
            'join_date' : ['join_date'],
            'sal_info' : sal_info,
            'total' : total
        })  
        
    return render(request,'search_eT_Invoice.html')

def search_Client_Invoice(request):
    return render(request,'search_Client_Invoice.html')

def search_Salary_Slip(request):
    return render(request,'search_Salary_Slip.html')

def logout(request):
    if 'role' in request.session:
        del request.session['role']
    
    return redirect('login')