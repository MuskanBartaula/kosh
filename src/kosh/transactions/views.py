from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from nepali_date import NepaliDate

from kosh.members.models import Member
from kosh.savings.models import MonthlySaving
from .forms import TransactionForm, AddMemberToTransactionForm
from .models import Transaction


@login_required
def add_member_to_transaction(request):
    template_name = "transactions/add_member_to_transaction.html"
    form = AddMemberToTransactionForm(request.POST or None)

    if form.is_valid():
        member_id = form.cleaned_data.get('member_id')
        return redirect('transactions:create', member_id=member_id)
    context = {
        'form': form,
    }

    return render(request, template_name, context)

class TransactionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Transaction
    template_name = "transactions/transaction_form.html"
    form_class = TransactionForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        try:
            member_obj = self.get_member()
        except Member.DoesNotExist:
            messages.warning(request, "Perhaps the member doesn't exists.")
            return redirect('/members/')
        try:
            monthly_saving_obj = MonthlySaving.objects.latest('timestamp')
        except MonthlySaving.DoesNotExist:
            messages.warning(request, "First you must provide the amount for monthly saving")
            return redirect('members:monthly_saving')
        return super().get(request, *args, **kwargs)

    def get_member(self):
        member_id = self.kwargs.get('member_id')
        member_obj = Member.objects.get(membership_id=member_id)
        return member_obj

    def get_initial(self):
        member = self.get_member()
        try:
            member_loan = Loan.objects.get(member=member).amount
        except Loan.DoesNotExist:
            member_loan = 0.00

        monthly_saving_obj = MonthlySaving.objects.latest('timestamp')
        member_monthly_saving = member.number_of_share * monthly_saving_obj.amount
        initial_data = {
            'member': self.get_member().id,
            'previous_month_loan': member_loan,
            'monthly_saving': member_monthly_saving,
        }
        return initial_data

    def get_context_data(self, **kwargs):
        context = super(TransactionCreateView, self).get_context_data(**kwargs)
        context['member'] = self.get_member()
        query = self.get_member().transaction_set.last()
        if query is not None:
            date = query.date
            nepali_date = NepaliDate.to_nepali_date(date)
            context['last_paid_date'] = nepali_date
        return context

class TransactionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "transactions/transaction_form.html"
    success_url = '/'

    def get_initial(self):
        date = self.get_object().date
        np_date = str(NepaliDate.to_nepali_date(date).strfdate("%Y-%m-%d"))

        initial_data = {
            'date': np_date
        }

        return initial_data

    def form_valid(self, form):
        current_transaction = self.get_object()
        upcoming_transactions = Transaction.objects.filter(
            member=current_transaction.member,
            date__gt=current_transaction.date,
        ).order_by('date')
        previous_month_loan = form.cleaned_data.get('total_loan_amount')
        prev_transaction = current_transaction
        for transaction in upcoming_transactions:
            transaction.previous_month_loan = previous_month_loan 
            transaction.save()
            prev_transaction = transaction
            previous_month_loan = prev_transaction.total_loan_amount

        return super(TransactionUpdateView, self).form_valid(form)


@login_required
def transaction_voucher(request, id):
    try:
        transaction = Transaction.objects.get(id=id)
    except Transaction.DoesNotExist:
        messages.warning(request, "Perhaps the member doesn't exists.")
        return redirect('members:index')
    context = {
        'transaction': transaction,
    }
    return render(request, "transactions/voucher.html", context)
