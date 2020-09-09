from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic


from nepali_date import NepaliDate


from loans.models import Loan
from members.models import Member, MonthlySaving
from .forms import TransactionForm, AddMemberToTransactionForm
from .models import Transaction


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

class TransactionCreateView(generic.CreateView):
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


def transaction_voucher(request, id):
    transaction = Transaction.objects.get(id=id)
    context = {
        'transaction': transaction,
    }
    return render(request, "transactions/voucher.html", context)
