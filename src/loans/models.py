from django.db import models

from members.models import Member

class Loan(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                default=0.00)

    def __str__(self):
        return self.member.name + " loan"
