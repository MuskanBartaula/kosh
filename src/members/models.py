from django.db import models
from django.core.exceptions import ValidationError

class MonthlySaving(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)
    
    def clean(self, *args, **kwargs):
        if not self.pk and MonthlySaving.objects.exists():
            raise ValidationError(
                "MonthlySaving instance already exists.",
                code='invalid'
            )
        super().clean(*args, **kwargs)

    def full_clean(self, *args, **kwargs):
        return self.clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Member(models.Model):
    membership_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=120)
    number_of_share = models.PositiveIntegerField()

    def __str__(self):
        return self.name
