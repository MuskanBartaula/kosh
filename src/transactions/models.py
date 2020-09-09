from django.db import models
from django.db.models.signals import post_save

from nepali_date import NepaliDate
from kosh.utils import split_date
from loans.models import Loan
from members.models import Member


class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    monthly_saving = models.DecimalField(max_digits=10, decimal_places=2)
    previous_month_loan = models.DecimalField(max_digits=10, decimal_places=2,
                                             default=0.00)
    interest = models.DecimalField(max_digits=10, decimal_places=2,
                                   default=0.00)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    others = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    loan_amount_paid = models.DecimalField(max_digits=10, decimal_places=2,
                                           blank=True, null=True,
                                           default=0.00)
    remaining_loan_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                           default=0.00)
    additional_loan_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                                 default=0.00)
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2,
                                            blank=True)
    total_loan_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                            default=0.00)
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.member.name + " transactions"

def transaction_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        loan_qs = Loan.objects.filter(member=instance.member)
        if loan_qs.exists():
            loan_obj = loan_qs.first()
            loan_obj.amount = instance.total_loan_amount
            loan_obj.save()
        else:
            loan_obj = Loan.objects.create(
                member=instance.member,
                amount=instance.total_loan_amount
            )

post_save.connect(transaction_post_save_receiver, sender=Transaction)
