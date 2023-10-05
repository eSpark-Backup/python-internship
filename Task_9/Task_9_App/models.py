from django.db import models

# Create your models here.
class eT_Invoice(models.Model):

    invoice_no = models.CharField(max_length=15, unique=True)
    attention = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    company_address = models.CharField(max_length=70)
    date=models.CharField(max_length=15)
    month=models.CharField(max_length=15)
    emp_info=models.JSONField()
    sal_info=models.JSONField()

    def save(self, *args, **kwargs):

        import datetime
        current_year = str(datetime.datetime.now().year)

        if not self.invoice_no:
            latest_invoice = eT_Invoice.objects.filter(
                invoice_no__startswith="ES-"+current_year+"-"
            ).order_by("-invoice_no").first()

            if latest_invoice:
                numeric_part = int(latest_invoice.invoice_no.split("-")[-1])
                numeric_part += 1
            else:
                numeric_part = 0

            self.invoice_no = f"ES-2023-{numeric_part:06}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_no
