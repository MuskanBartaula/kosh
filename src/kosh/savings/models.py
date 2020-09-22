from django.db import models

class MonthlySaving(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        if not self.pk and MonthlySaving.objects.exists():
            raise ValueError("MonthlySaving instance already exists.")
        return super().save(*args, **kwargs)

