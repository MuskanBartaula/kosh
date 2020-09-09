from django.shortcuts import render, redirect

from members.models import Member
from .forms import LoanForm
from .models import Loan

def add_loan_amount(request):
    form = LoanForm(request.POST or None)
    if form.is_valid():
        membership_id = form.cleaned_data.get('membership_id')
        loan_amount = form.cleaned_data.get('amount')

        member_obj = Member.objects.get(membership_id=membership_id)

        member_loan_qs = Loan.objects.filter(member=member_obj)
        if member_loan_qs.exists():
            loan_obj = member_loan_qs.first()
            total_loan_amount = float(loan_obj.amount) + float(loan_amount)
            loan_obj.amount = total_loan_amount
            loan_obj.save()
        else:
            loan_obj = Loan.objects.create(member=member_obj, amount=loan_amount)

        return redirect(request.path)

    context = {
        'form': form,
    }
    return render(request, 'loans/loan_form.html', context)
