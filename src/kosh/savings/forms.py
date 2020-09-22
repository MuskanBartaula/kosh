from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Submit,
    ButtonHolder,
    Field
)

from .models import MonthlySaving

class MonthlySavingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'] = forms.CharField()
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Field('amount', autocomplete="off"),

            ButtonHolder(
                Submit('submit', 'Submit', css_class="btn btn-success"),
                
            )
        )
    class Meta:
        model = MonthlySaving
        fields = ('amount', )

    def clean(self):
        data = self.cleaned_data
        monthly_saving_exists = MonthlySaving.objects.exists()
        if self.instance:
            monthly_saving_exists = MonthlySaving.objects.exclude(pk=self.instance.pk)
        if monthly_saving_exists:
            raise forms.ValidationError("MonthlySaving instance already exists.")
        return data


