from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Submit,
    ButtonHolder,
    Field
)

from .models import Member

class MemberForm(forms.ModelForm):
    previous_due = forms.DecimalField(decimal_places=2,
                                      max_digits=20, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['membership_id'].widget = forms.TextInput()
        self.fields['number_of_share'].widget = forms.TextInput()
        self.fields['previous_due'].widget = forms.TextInput()
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Field('membership_id', autocomplete="off"),
            Field('name', autocomplete="off"),
            Field('number_of_share', autocomplete="off"),
            Field('previous_due', autocomplete="off"),

            ButtonHolder(
                Submit('submit', 'Submit', css_class="btn btn-success btn-block")
            )
        )


    class Meta:
        model = Member
        fields = (
            'membership_id',
            'name',
            'number_of_share',
        )
