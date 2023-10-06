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
        ser_char_hours = int(request.POST['ser_char_hours'])
        ser_char_per_hour = int(request.POST['ser_char_per_hour'])
        man_char_hours = int(request.POST['man_char_hours'])
        man_char_per_hour = int(request.POST['man_char_per_hour'])

        ser_char_amount = ser_char_hours*ser_char_per_hour
        man_char_amount = man_char_hours*man_char_per_hour

        total = ser_char_amount+man_char_amount

        emp_info={
            'emp_id':emp_id,
            'emp_name':emp_name,
            'emp_desig':emp_desig,
            'proj_name':proj_name,
            'job_mode':job_mode
        }

        sal_info={
            'services':['Service Charges','Management Fee'],
            'hours':[ser_char_hours,man_char_hours],
            'hourly rate':[ser_char_per_hour,man_char_per_hour],
            'amount':[ser_char_amount,man_char_amount]
        }

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
        b_pay_earn_amount=int(request.POST['b_pay_earn_amount'])
        ded_rec_1=(request.POST['ded_rec_1'])
        ded_rec_1_amount=int(request.POST['ded_rec_1_amount'])
        sp_tech_earn_amount=int(request.POST['sp_tech_earn_amount'])
        ded_rec_2=(request.POST['ded_rec_2'])
        ded_rec_2_amount=int(request.POST['ded_rec_2_amount'])
        punct_earn_amount=int(request.POST['punct_earn_amount'])
        ded_rec_3=(request.POST['ded_rec_3'])
        ded_rec_3_amount=int(request.POST['ded_rec_3_amount'])
        mg_allow_earn_amount=int(request.POST['mg_allow_earn_amount'])
        ded_rec_4=(request.POST['ded_rec_4'])
        ded_rec_4_amount=int(request.POST['ded_rec_4_amount'])
        proj_earn_amount=int(request.POST['proj_earn_amount'])
        ded_rec_5=(request.POST['ded_rec_5'])
        ded_rec_5_amount=int(request.POST['ded_rec_5_amount'])
        convey_allow_earn_amount=int(request.POST['convey_allow_earn_amount'])
        ded_rec_6=(request.POST['ded_rec_6'])
        ded_rec_6_amount=int(request.POST['ded_rec_6_amount'])
        onsite_allow_earn_amount=int(request.POST['onsite_allow_earn_amount'])
        ded_rec_7=(request.POST['ded_rec_7'])
        ded_rec_7_amount=int(request.POST['ded_rec_7_amount'])

        total_earn=b_pay_earn_amount+sp_tech_earn_amount+punct_earn_amount+mg_allow_earn_amount+proj_earn_amount+convey_allow_earn_amount+onsite_allow_earn_amount

        total_deduc=ded_rec_1_amount+ded_rec_2_amount+ded_rec_3_amount+ded_rec_4_amount+ded_rec_5_amount+ded_rec_7_amount

        sal_info={
            'earning description':['Basic Pay','Special Tech Allowance','Punctuality','Management Allowance','Project Allowance','Conveyance Allowance','On Site Allowance'],
            'Earn Amount':[b_pay_earn_amount,sp_tech_earn_amount,punct_earn_amount,mg_allow_earn_amount,proj_earn_amount,convey_allow_earn_amount,onsite_allow_earn_amount],
            'deduction recoveries':[ded_rec_1,ded_rec_2,ded_rec_3,ded_rec_4,ded_rec_5,ded_rec_6,ded_rec_7],
            'Deduct Amount':[ded_rec_1_amount,ded_rec_2_amount,ded_rec_3_amount,ded_rec_4_amount,ded_rec_5_amount,ded_rec_6_amount,ded_rec_7_amount]
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
            "b_pay_earn_amount":b_pay_earn_amount,
            "ded_rec_1":ded_rec_1,
            "ded_rec_1_amount":ded_rec_1_amount,
            "sp_tech_earn_amount":sp_tech_earn_amount,
            "ded_rec_2":ded_rec_2,
            "ded_rec_2_amount":ded_rec_2_amount,
            "punct_earn_amount":punct_earn_amount,
            "ded_rec_3":ded_rec_3,
            "ded_rec_3_amount":ded_rec_3_amount,
            "mg_allow_earn_amount":mg_allow_earn_amount,
            "ded_rec_4":ded_rec_4,
            "ded_rec_4_amount":ded_rec_4_amount,
            "proj_earn_amount":proj_earn_amount,
            "ded_rec_5":ded_rec_5,
            "ded_rec_5_amount":ded_rec_5_amount,
            "convey_allow_earn_amount":convey_allow_earn_amount,
            "ded_rec_6":ded_rec_6,
            "ded_rec_6_amount":ded_rec_6_amount,
            "onsite_allow_earn_amount":onsite_allow_earn_amount,
            "ded_rec_7":ded_rec_7,
            "ded_rec_7_amount":ded_rec_7_amount,
            "total_earn":total_earn,
            "total_deduc":total_deduc,
            "net_pay":net_pay
        })


    return render(request,'Salary_Slip.html')

@login_admin_successfull
def Client_Invoice(request):
    if request.method=='POST':

        inv_recipient=request.POST["inv_recipient"]
        attention=request.POST["attention"]
        invoice_no=request.POST["invoice_no"]
        prep_by=request.POST["prep_by"]
        date=request.POST["date"]
        contact_per=request.POST["contact_per"]
        email=request.POST["email"]
        item_1=request.POST["item_1"]
        specs_1=request.POST["specs_1"]
        qty_1=int(request.POST["qty_1"])
        price_1=int(request.POST["price_1"])
        item_2=request.POST["item_2"]
        specs_2=request.POST["specs_2"]
        qty_2=int(request.POST["qty_2"])
        price_2=int(request.POST["price_2"])
        item_3=request.POST["item_3"]
        specs_3=request.POST["specs_3"]
        qty_3=int(request.POST["qty_3"])
        price_3=int(request.POST["price_3"])

        amount_1=qty_1*price_1
        amount_2=qty_2*price_2
        amount_3=qty_3*price_3

        total=amount_1+amount_2+amount_3

        new_client_invoice=Client_Invoice_Table.objects.create(invoice_no=invoice_no,inv_recipient=inv_recipient,attention=attention,prep_by=prep_by,date=date,contact_per=contact_per,email=email)

        return render(request, 'Client_Invoice_pdf.html', {
            "inv_recipient":inv_recipient,
            "attention":attention,
            "invoice_no":invoice_no,
            "prep_by":prep_by,
            "date":date,
            "contact_per":contact_per,
            "email":email,
            "item_1":item_1,
            "specs_1":specs_1,
            "qty_1":qty_1,
            "price_1":price_1,
            "amount_1":amount_1,
            "item_2":item_2,
            "specs_2":specs_2,
            "qty_2":qty_2,
            "price_2":price_2,
            "amount_2":amount_2,
            "item_3":item_3,
            "specs_3":specs_3,
            "qty_3":qty_3,
            "price_3":price_3,
            "amount_3":amount_3,
            "total":total,
        })


    return render(request,'Client_Invoice.html')

def logout(request):
    if 'role' in request.session:
        del request.session['role']
    
    return redirect('login')