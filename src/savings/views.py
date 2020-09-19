from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic

from .forms import MonthlySavingForm
from .models import MonthlySaving

@login_required
def monthly_saving(request):
    monthly_saving_exists = MonthlySaving.objects.exists()
    if monthly_saving_exists:
        instance = MonthlySaving.objects.first()
        return redirect('savings:update', pk=instance.pk)
    return redirect('savings:add')


class MonthlySavingCreateView(LoginRequiredMixin, generic.CreateView):
    model = MonthlySaving
    template_name = "members/monthly_saving_form.html"
    form_class = MonthlySavingForm
    success_url = '/'


class MonthlySavingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = MonthlySaving
    template_name = "members/monthly_saving_form.html"
    form_class = MonthlySavingForm

    def get_success_url(self):
        messages.success(self.request, "Monthly saving amount successfully updated !!!")
        return reverse('members:monthly_saving_update', kwargs={'pk': self.object.pk})
