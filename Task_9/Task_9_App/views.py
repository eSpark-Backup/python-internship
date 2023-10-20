from django.shortcuts import render,redirect
from .decorators import *
from django.views.decorators.cache import cache_control
from . models import eT_Invoice_Table,Salary_Slip_Table,Client_Invoice_Table

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'eSparkAdmin' and password == 'admin@espark':
            request.session['role'] = 'admin'
            request.session['template_name'] = 'home_admin'  # Set the template_name for admin
            return redirect("admin_home", template_name='home_admin')

        if username == 'eSparkFinanceDept' and password == 'financeDept@espark':
            request.session['role'] = 'finance'
            request.session['template_name'] = 'home_finance'  # Set the template_name for finance
            return redirect("finance_home", template_name='home_finance')

        if username == 'eSparkHrDept' and password == 'hrDept@espark':
            request.session['role'] = 'hr'
            request.session['template_name'] = 'home_hr'  # Set the template_name for hr
            return redirect("hr_home", template_name='home_hr')

        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response

@login_admin_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_home(request, template_name):
    try:
        template_name='home_admin'
        return render(request,f'{template_name}.html')
    except:
        return render(request, 'home_admin.html')

@login_finance_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def finance_home(request, template_name):
    template_name='home_finance'
    return render(request,f'{template_name}.html')

@login_hr_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hr_home(request, template_name):
    template_name='home_hr'
    return render(request,f'{template_name}.html')

@login_adminorhr_successfull
def add_emp(request):
    return render(request,'Add_Emp.html')

@login_adminorfinance_successfull
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

@login_adminorfinance_successfull
def search_eT_Invoice(request):
    return render(request,'search_eT_Invoice.html')

@login_adminorfinance_successfull
def view_eT_Invoice(request):
    if request.method=='POST':
        inv_no=request.POST['inv_no']

        try:
            invoice_data = eT_Invoice_Table.objects.get(invoice_no=inv_no)
        except eT_Invoice_Table.DoesNotExist:
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

            request.session['current_invoice_number']= inv_no
            request.session['attention']= attention
            request.session['company_name']= company_name
            request.session['email']= email
            request.session['company_address']= company_address
            request.session['date']= date
            request.session['month']= month
            request.session['emp_id']= emp_info['emp_id']
            request.session['emp_name']= emp_info['emp_name']
            request.session['emp_desig']=emp_info['emp_desig']
            request.session['proj_name']= emp_info['proj_name']
            request.session['job_mode']= emp_info['job_mode']
            request.session['join_date']= emp_info['join_date']
            request.session['sal_info']= sal_info
            request.session['total']= total
            
            return render(request, 'view_eT_Invoice.html', {
            'current_invoice_number' : inv_no,
            'attention' : attention,
            'company_name' : company_name,
            'email' : email,
            'company_address' : company_address,
            'date' : date,
            'month' : month,
            'emp_id' : emp_info['emp_id'],
            'emp_name' : emp_info['emp_name'],
            'emp_desig':emp_info['emp_desig'],
            'proj_name' : emp_info['proj_name'],
            'job_mode' : emp_info['job_mode'],
            'join_date' : emp_info['join_date'],
            'sal_info' : sal_info,
            'total' : total
        })
        
        else:
            return render(request, 'search_eT_Invoice.html', {'error_message': 'Invalid Invoice Number'})  

@login_adminorfinance_successfull
def edit_eT_Invoice(request):
    if request.method=='POST':
        inv_no=request.POST['inv_no']

        invoice_data = eT_Invoice_Table.objects.get(invoice_no=inv_no)

        attention=request.POST.get('attention')
        company_name=request.POST.get('comp_name')
        email=request.POST.get('email')
        company_address=request.POST.get('comp_addr')
        date=request.POST.get('date')
        month=request.POST.get('inv_month')
        emp_id=request.POST.get('emp_id')
        emp_name=request.POST.get('emp_name')
        emp_desig=request.POST.get('emp_desig')
        proj_name=request.POST.get('proj_name')
        job_mode=request.POST.get('job_mode')
        join_date=request.POST.get('join_date')
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

        invoice_data.attention=attention
        invoice_data.company_name=company_name
        invoice_data.email=email
        invoice_data.company_address=company_address
        invoice_data.date=date
        invoice_data.month=month
        invoice_data.emp_info=emp_info
        invoice_data.sal_info=sal_info
        invoice_data.save()
        total = sum(sal_info['amounts'])

        request.session['attention'] = attention
        request.session['company_name'] = company_name
        request.session['email'] = email
        request.session['company_address'] = company_address
        request.session['date'] = date
        request.session['month'] = month
        request.session['emp_id'] = emp_info['emp_id']
        request.session['emp_name'] = emp_info['emp_name']
        request.session['emp_desig'] = emp_info['emp_desig']
        request.session['proj_name'] = emp_info['proj_name']
        request.session['job_mode'] = emp_info['job_mode']
        request.session['join_date'] = emp_info['join_date']
        request.session['sal_info'] = sal_info
        request.session['total'] = total


        return render(request, 'view_eT_Invoice.html', {
            'current_invoice_number' : inv_no,
            'attention' : attention,
            'company_name' : company_name,
            'email' : email,
            'company_address' : company_address,
            'date' : date,
            'month' : month,
            'emp_id' : emp_info['emp_id'],
            'emp_name' : emp_info['emp_name'],
            'emp_desig':emp_info['emp_desig'],
            'proj_name' : emp_info['proj_name'],
            'job_mode' : emp_info['job_mode'],
            'join_date' : emp_info['join_date'],
            'sal_info' : sal_info,
            'total' : total
        })

    inv_no=request.session.get('current_invoice_number')
    attention=request.session.get('attention')
    company_name=request.session.get('company_name')
    email=request.session.get('email')
    company_address=request.session.get('company_address')
    date=request.session.get('date')
    month=request.session.get('month')
    emp_id=request.session.get('emp_id')
    emp_name=request.session.get('emp_name')
    emp_desig=request.session.get('emp_desig')
    proj_name=request.session.get('proj_name')
    job_mode=request.session.get('job_mode')
    join_date=request.session.get('join_date')
    sal_info=request.session.get('sal_info')
    total=request.session.get('total')

    return render(request, 'edit_eT_Invoice.html', {
            'current_invoice_number' : inv_no,
            'attention' : attention,
            'company_name' : company_name,
            'email' : email,
            'company_address' : company_address,
            'date' : date,
            'month' : month,
            'emp_id' : emp_id,
            'emp_name' : emp_name,
            'emp_desig': emp_desig,
            'proj_name' : proj_name,
            'job_mode' : job_mode,
            'join_date' : join_date,
            'sal_info' : sal_info,
            'total' : total
        })

@login_adminorfinance_successfull
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
        deduct_amount = [int(amount) if amount else 0 for amount in request.POST.getlist('deduct_amount[]')]
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

@login_adminorfinance_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_Salary_Slip(request):
    return render(request,'search_Salary_Slip.html')

@login_adminorfinance_successfull
def view_Salary_Slip(request):
    if request.method=='POST':
        emp_id=request.POST['emp_id']
        month=request.POST['payroll_month']
        
        try:
            salary_slip_data = Salary_Slip_Table.objects.get(emp_id=emp_id, payroll_month=month)
        except Salary_Slip_Table.DoesNotExist:
            salary_slip_data = None

        if salary_slip_data!=None:
            emp_id=emp_id
            emp_name=salary_slip_data.emp_name
            desig=salary_slip_data.desig
            tot_ser=salary_slip_data.tot_ser
            join_date=salary_slip_data.join_date
            payroll_month=month
            status=salary_slip_data.status
            email=salary_slip_data.email
            phone_no=salary_slip_data.phone_no
            bank_acc=salary_slip_data.bank_acc
            nok=salary_slip_data.nok
            sal_info=salary_slip_data.sal_info
            total_earn=sum(sal_info['Earn_Amount'])
            total_deduc=sum(sal_info['Deduct_Amount'])
            net_pay=total_earn-total_deduc

            request.session['emp_id'] = emp_id
            request.session['emp_name'] = salary_slip_data.emp_name
            request.session['desig'] = salary_slip_data.desig
            request.session['tot_ser'] = salary_slip_data.tot_ser
            request.session['join_date'] = salary_slip_data.join_date
            request.session['payroll_month'] = month
            request.session['status'] = salary_slip_data.status
            request.session['email'] = salary_slip_data.email
            request.session['phone_no'] = salary_slip_data.phone_no
            request.session['bank_acc'] = salary_slip_data.bank_acc
            request.session['nok'] = salary_slip_data.nok
            request.session['sal_info'] = sal_info
            request.session['total_earn'] = total_earn
            request.session['total_deduc'] = total_deduc
            request.session['net_pay'] = net_pay

            return render(request,'view_Salary_Slip.html',{
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
        
        else:
            return render(request, 'search_Salary_Slip.html', {'error_message': 'Invalid Employee ID or Month'})

@login_adminorfinance_successfull
def edit_Salary_Slip(request):
    if request.method=='POST':
        emp_id=request.POST['emp_id']
        month=request.POST['payroll_month']

        salary_slip_data = Salary_Slip_Table.objects.get(emp_id=emp_id, payroll_month=month)

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
        deduct_amount = [int(amount) if amount else 0 for amount in request.POST.getlist('deduct_amount[]')]

        total_earn = sum(earn_amount)
        total_deduc = sum(deduct_amount)

        sal_info={
            'Earning_Description' : earnings,
            'Earn_Amount' : earn_amount,
            'Deduction_Recoveries' : deductions,
            'Deduct_Amount' : deduct_amount
        }

        net_pay= total_earn - total_deduc

        salary_slip_data.emp_id=emp_id
        salary_slip_data.emp_name=emp_name
        salary_slip_data.desig=desig
        salary_slip_data.tot_ser=tot_ser
        salary_slip_data.join_date=join_date
        salary_slip_data.payroll_month=payroll_month
        salary_slip_data.status=status
        salary_slip_data.email=email
        salary_slip_data.phone_no=phone_no
        salary_slip_data.bank_acc=bank_acc
        salary_slip_data.nok=nok
        salary_slip_data.sal_info=sal_info
        salary_slip_data.save()

        request.session['emp_id'] = emp_id
        request.session['emp_name'] = salary_slip_data.emp_name
        request.session['desig'] = salary_slip_data.desig
        request.session['tot_ser'] = salary_slip_data.tot_ser
        request.session['join_date'] = salary_slip_data.join_date
        request.session['payroll_month'] = month
        request.session['status'] = salary_slip_data.status
        request.session['email'] = salary_slip_data.email
        request.session['phone_no'] = salary_slip_data.phone_no
        request.session['bank_acc'] = salary_slip_data.bank_acc
        request.session['nok'] = salary_slip_data.nok
        request.session['sal_info'] = sal_info
        request.session['total_earn'] = total_earn
        request.session['total_deduc'] = total_deduc
        request.session['net_pay'] = net_pay

        return render(request,'view_Salary_Slip.html',{
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

    emp_id = request.session.get('emp_id')
    emp_name = request.session.get('emp_name')
    desig = request.session.get('desig')
    tot_ser = request.session.get('tot_ser')
    join_date = request.session.get('join_date')
    payroll_month = request.session.get('payroll_month')
    status = request.session.get('status')
    email = request.session.get('email')
    phone_no = request.session.get('phone_no')
    bank_acc = request.session.get('bank_acc')
    nok = request.session.get('nok')
    sal_info = request.session.get('sal_info')
    total_earn = request.session.get('total_earn')
    total_deduc = request.session.get('total_deduc')
    net_pay = request.session.get('net_pay')

    return render(request,'edit_Salary_Slip.html',{
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


@login_adminorfinance_successfull
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

@login_adminorfinance_successfull
def search_Client_Invoice(request):
    return render(request,'search_Client_Invoice.html')

@login_adminorfinance_successfull
def view_Client_Invoice(request):
    if request.method=='POST':
        inv_no=request.POST['inv_no']

        try:
            invoice_data = Client_Invoice_Table.objects.get(invoice_no=inv_no)
        except Client_Invoice_Table.DoesNotExist:
            invoice_data = None

        if invoice_data!=None:
            inv_recipient=invoice_data.inv_recipient
            attention=invoice_data.attention
            prep_by=invoice_data.prep_by
            date=invoice_data.date
            contact_per=invoice_data.contact_per
            email=invoice_data.email
            item_desc=invoice_data.item_desc
            total = sum(item_desc['amounts'])

            request.session['inv_recipient'] = inv_recipient
            request.session['attention'] = attention
            request.session['invoice_no'] = inv_no
            request.session['prep_by'] = prep_by
            request.session['date'] = date
            request.session['contact_per'] = contact_per
            request.session['email'] = email
            request.session['item_desc'] = item_desc
            request.session['total'] = total

            return render(request, 'view_Client_Invoice.html', {
                "inv_recipient":inv_recipient,
                "attention":attention,
                "invoice_no":inv_no,
                "prep_by":prep_by,
                "date":date,
                "contact_per":contact_per,
                "email":email,
                "item_desc": item_desc,
                "total":total
            })
        
        else:
            return render(request, 'search_Client_Invoice.html', {'error_message': 'Invalid Invoice Number'})

@login_adminorfinance_successfull
def edit_Client_Invoice(request):
    if request.method=='POST':
        inv_no=request.POST['inv_no']

        invoice_data = Client_Invoice_Table.objects.get(invoice_no=inv_no)

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

        invoice_data.inv_recipient=inv_recipient
        invoice_data.attention=attention
        invoice_data.prep_by=prep_by
        invoice_data.date=date
        invoice_data.contact_per=contact_per
        invoice_data.email=email
        invoice_data.item_desc=item_desc

        invoice_data.save()

        request.session['inv_recipient'] = inv_recipient
        request.session['attention'] = attention
        request.session['invoice_no'] = inv_no
        request.session['prep_by'] = prep_by
        request.session['date'] = date
        request.session['contact_per'] = contact_per
        request.session['email'] = email
        request.session['item_desc'] = item_desc
        request.session['total'] = total            
        
        return render(request, 'view_Client_Invoice.html', {
                "inv_recipient":inv_recipient,
                "attention":attention,
                "invoice_no":inv_no,
                "prep_by":prep_by,
                "date":date,
                "contact_per":contact_per,
                "email":email,
                "item_desc": item_desc,
                "total":total
            })
        
    inv_recipient = request.session.get('inv_recipient')
    attention = request.session.get('attention')
    inv_no = request.session.get('invoice_no')
    prep_by = request.session.get('prep_by')
    date = request.session.get('date')
    contact_per = request.session.get('contact_per')
    email = request.session.get('email')
    item_desc = request.session.get('item_desc')
    total = request.session.get('total')

    return render(request, 'edit_Client_Invoice.html', {
                "inv_recipient":inv_recipient,
                "attention":attention,
                "invoice_no":inv_no,
                "prep_by":prep_by,
                "date":date,
                "contact_per":contact_per,
                "email":email,
                "item_desc": item_desc,
                "total":total
            })

def logout(request):
    if 'role' in request.session:
        del request.session['role']
    
    return redirect('login')