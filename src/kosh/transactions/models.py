from django.db import models
from django.db.models.signals import post_save

from nepali_date import NepaliDate
from kosh.core.utils import split_date
from kosh.members.models import Member


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

    def save(self, *args, **kwargs):
        self.remaining_loan_amount = self.previous_month_loan - self.loan_amount_paid
        self.total_loan_amount = self.remaining_loan_amount + self.additional_loan_amount
        return super().save(*args, **kwargs)
