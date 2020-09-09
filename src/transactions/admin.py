from django.contrib import admin

from .models import Transaction

class TransactionModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Transaction, TransactionModelAdmin)
