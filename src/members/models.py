from django.db import models

class MonthlySaving(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)


class Member(models.Model):
    membership_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=120)
    number_of_share = models.PositiveIntegerField()

    def __str__(self):
        return self.name
