from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse

from .forms import MemberForm, MonthlySavingForm
from .models import Member, MonthlySaving


class MemberMixin(object):
    def get_context_data(self, **kwargs):
        context = super(MemberMixin, self).get_context_data(**kwargs)
        context['object_list'] = Member.objects.all()
        return context

    def get_success_url(self):
        return reverse('members:index')


def monthly_saving(request):
    monthly_saving_exists = MonthlySaving.objects.exists()
    if monthly_saving_exists:
        instance = MonthlySaving.objects.first()
        return redirect(f'/members/monthly-saving/update/{instance.pk}')
    return redirect('members:monthly_saving_add')


class MonthlySavingCreateView(generic.CreateView):
    model = MonthlySaving
    template_name = "members/monthly_saving_form.html"
    form_class = MonthlySavingForm
    success_url = '/'


class MonthlySavingUpdateView(generic.UpdateView):
    model = MonthlySaving
    template_name = "members/monthly_saving_form.html"
    form_class = MonthlySavingForm
    success_url = '/'


class MemberCreateView(MemberMixin, SuccessMessageMixin, generic.CreateView):
    model = Member
    template_name = 'members/index.html'
    form_class = MemberForm
    success_message = 'Member "%(name)s" successfully created.'


class MemberListView(generic.ListView):
    model = Member


class MemberUpdateView(MemberMixin, SuccessMessageMixin,  generic.UpdateView):
    model = Member
    template_name = "members/member_form.html"
    form_class = MemberForm
    success_message = 'Member "%(name)s" successfully updated.'


class MemberDeleteView(MemberMixin, generic.DeleteView):
    model = Member
    template_name = "members/member_confirm_delete.html"
