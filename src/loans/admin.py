from django.contrib import admin

from .models import Loan

class LoanModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Loan, LoanModelAdmin)
