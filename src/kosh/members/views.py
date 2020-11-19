from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse

from kosh.loans.models import Loan
from .forms import MemberForm
from .models import Member


class MemberMixin(object):
    def get_context_data(self, **kwargs):
        context = super(MemberMixin, self).get_context_data(**kwargs)
        context['object_list'] = Member.objects.all().order_by('membership_id')
        return context

    def get_success_url(self):
        return reverse('members:index')

class LoginSuccessMessageMixin(LoginRequiredMixin, SuccessMessageMixin):
    pass

class MemberCreateView(LoginSuccessMessageMixin, MemberMixin, generic.CreateView):
    model = Member
    template_name = 'members/index.html'
    form_class = MemberForm
    success_message = 'Member "%(name)s" successfully created.'

    def form_valid(self, form):
        previous_due = form.cleaned_data.get('previous_due')
        member_id = form.cleaned_data.get('membership_id')
        self.object = form.save()
        loan_obj = Loan.objects.create(member_id=self.object.id, amount=previous_due)
        return redirect('members:index')


class MemberListView(generic.ListView):
    model = Member


class MemberUpdateView(LoginSuccessMessageMixin, MemberMixin, generic.UpdateView):
    model = Member
    template_name = "members/member_form.html"
    form_class = MemberForm
    success_message = 'Member "%(name)s" successfully updated.'

    def get_initial(self):
        member_loan_qs = Loan.objects.filter(member_id=self.object.id)
        previous_due = 0.00
        if member_loan_qs.exists():
            member_loan_obj = member_loan_qs.first()
            previous_due = member_loan_obj.amount
        initial_data = {'previous_due': previous_due}
        return initial_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_update'] = True
        return context


class MemberDeleteView(LoginRequiredMixin, MemberMixin, generic.DeleteView):
    model = Member
    template_name = "members/member_confirm_delete.html"
