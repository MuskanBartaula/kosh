from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save

from nepali_date import NepaliDate
from kosh.core.utils import split_date
from kosh.loans.models import Loan
from kosh.members.models import Member
from kosh.savings.models import MemberSaving


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


def transaction_post_save_receiver(sender, instance, created, *args, **kwargs):	
    transactions = Transaction.objects.filter(member=instance.member)
    total_savings_dict = transactions.aggregate(total_savings=Sum('monthly_saving'))
    total_savings = total_savings_dict.get('total_savings')

    member_savings = MemberSaving.objects.filter(member=instance.member)
    if member_savings.exists():
        member_saving_obj = member_savings.first()
        member_saving_obj.amount = total_savings
        member_saving_obj.save()
    else:
        MemberSaving.objects.create(member=instance.member, amount=total_savings)

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
