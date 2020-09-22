from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse

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


class MemberListView(generic.ListView):
    model = Member


class MemberUpdateView(LoginSuccessMessageMixin, MemberMixin, generic.UpdateView):
    model = Member
    template_name = "members/member_form.html"
    form_class = MemberForm
    success_message = 'Member "%(name)s" successfully updated.'


class MemberDeleteView(LoginRequiredMixin, MemberMixin, generic.DeleteView):
    model = Member
    template_name = "members/member_confirm_delete.html"