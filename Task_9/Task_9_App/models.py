from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class eT_Invoice_Table(models.Model):

    current_date = models.DateField(default=timezone.now)
    invoice_no = models.CharField(max_length=15, unique=True)
    attention = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    email = models.CharField(max_length=20)
    company_address = models.CharField(max_length=70)
    date=models.CharField(max_length=15)
    month=models.CharField(max_length=15)
    emp_info=models.JSONField()
    sal_info=models.JSONField()

    def save(self, *args, **kwargs):

        
        current_year = str(datetime.datetime.now().year)

        if not self.invoice_no:
            latest_invoice = eT_Invoice_Table.objects.filter(
                invoice_no__startswith="ETI-"
            ).order_by("-invoice_no").first()

            if latest_invoice:
                numeric_part = int(latest_invoice.invoice_no.split("-")[-1])
                numeric_part += 1
            else:
                numeric_part = 1

            self.invoice_no = f"ETI-{current_year}-{numeric_part:02}"
        if not self.current_date:
            self.current_date=datetime.datetime.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_no


class Salary_Slip_Table(models.Model):

    current_date = models.DateField(default=timezone.now)
    emp_id = models.CharField(max_length=15)
    emp_name = models.CharField(max_length=50)
    desig = models.CharField(max_length=30)
    tot_ser = models.CharField(max_length=30)
    join_date=models.CharField(max_length=15)
    payroll_month=models.CharField(max_length=15)
    status=models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone_no=models.CharField(max_length=15)
    bank_acc=models.CharField(max_length=20)
    nok=models.CharField(max_length=20)
    sal_info=models.JSONField()

    def __str__(self):
        return self.emp_id

class Client_Invoice_Table(models.Model):

    current_date = models.DateField(default=timezone.now)
    invoice_no = models.CharField(max_length=15, unique=True)
    inv_recipient=models.CharField(max_length=50)
    attention=models.CharField(max_length=50)
    prep_by=models.CharField(max_length=50)
    date=models.CharField(max_length=15)
    contact_per=models.CharField(max_length=50)
    email=models.CharField(max_length=20)
    item_desc=models.JSONField()

    def save(self, *args, **kwargs):
        current_year = str(datetime.datetime.now().year)

        if not self.invoice_no:
            latest_invoice = Client_Invoice_Table.objects.filter(
                invoice_no__startswith="CI-"
            ).order_by("-invoice_no").first()

            if latest_invoice:
                numeric_part = int(latest_invoice.invoice_no.split("-")[-1])
                numeric_part += 1
            else:
                numeric_part = 1

            self.invoice_no = f"CI-{current_year}-{numeric_part:02}"
        if not self.current_date:
            self.current_date=datetime.datetime.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_no


class Employee_Table(models.Model):

    current_date = models.DateField(default=timezone.now)
    emp_id=models.CharField(max_length=15,unique=True)
    emp_name = models.CharField(max_length=50)
    desig = models.CharField(max_length=30)
    dept = models.CharField(max_length=30)
    status=models.CharField(max_length=20)
    job_mode=models.CharField(max_length=20)
    a_apoint=models.CharField(max_length=30)
    ff_name=models.CharField(max_length=50)
    general_info=models.JSONField()
    salary_info=models.JSONField()
    personal_info=models.JSONField()

    def save(self, *args, **kwargs):
        current_year = str(datetime.datetime.now().year)

        if not self.emp_id:
            latest_emp = Employee_Table.objects.filter(
                emp_id__startswith="eS-"
            ).order_by("-emp_id").first()

            if latest_emp:
                numeric_part = int(latest_emp.emp_id.split("-")[-1])
                numeric_part += 1
            else:
                numeric_part = 1

            self.emp_id = f"eS-{current_year}-{numeric_part:02}"
        if not self.current_date:
            self.current_date=datetime.datetime.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.emp_id
