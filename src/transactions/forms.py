import datetime

from django import forms
from django.core.validators import RegexValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, ButtonHolder, Submit,
    Field, Fieldset, Div
)
from nepali_date import NepaliDate

from kosh.utils import bs_to_ad, get_nepali_prev_month
from members.models import Member
from .models import Transaction

def instance_date_list_in_bs(instance_list):
    '''
        instance_list must be a queryset of model instance
        and must have a date field

        return the nepali date list of an instance date
    '''
    instance_date_list = []
    for instance in instance_list:
        instance_np_date = NepaliDate.to_nepali_date(instance.date)
        instance_date_list.append(instance_np_date)
    return instance_date_list

def transaction_month_exists(member, transaction_date):
    '''
        if transaction has already done on the same month in same year
            return True 
        else 
            return False

    '''
    member_transactions = Transaction.objects.filter(member=member)
    nep_transaction_date_list = instance_date_list_in_bs(member_transactions)
    for nep_member_transaction_date in nep_transaction_date_list:
        is_year_equal = transaction_date.year == nep_member_transaction_date.year
        is_month_equal = transaction_date.month == nep_member_transaction_date.month
        if is_year_equal and is_month_equal:
            return True
    return False

class AddMemberToTransactionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['member_id'].widget = forms.TextInput()

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Field('member_id', autocomplete="off"),
            ButtonHolder(
                Submit('submit', 'Submit', css_class="btn btn-success"),
            )
        )

    member_id = forms.IntegerField()

    def clean_member_id(self):
        member_id = self.cleaned_data.get('member_id')
        qs = Member.objects.filter(membership_id=member_id)
        if not qs.exists():
            raise forms.ValidationError("Member with this id doesn't exists.")
        return member_id


nepali_date_regex = '(^[12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[012])$)'

class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['member'].widget = forms.HiddenInput()
        self.fields['fine'].widget = forms.TextInput()
        self.fields['others'].widget = forms.TextInput()
        self.fields['loan_amount_paid'].widget = forms.TextInput()
        self.fields['additional_loan_amount'].widget = forms.TextInput()
        self.fields['date'] = forms.CharField(
            max_length=12,
            validators=[
                RegexValidator(
                  regex=nepali_date_regex,
                  message="Enter a valid date",
                )
            ]
        )
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-4"
        self.helper.field_class = "col-4"
        self.helper.layout = Layout(
            Fieldset(
                "Payment Transaction", 
                Field('monthly_saving', autocomplete="off", readonly="true"),
                Field('interest', autocomplete="off", readonly="true"),
                Field('fine', autocomplete="off"),
                Field('others', autocomplete="off"),
            ),

            Fieldset(
                "Loan Transaction",
                Field('member', autocomplete="off"),
                Field('previous_month_loan', autocomplete="off", readonly="true"),
                Field('loan_amount_paid', autocomplete="off"),
                Field('remaining_loan_amount', autocomplete="off", readonly="true"),
                Field('additional_loan_amount', autocomplete="off"),
                Field('total_loan_amount', autocomplete="off", readonly="true"),
            ),

            Field('total_amount_paid', autocomplete="off", readonly="true"),
            Field('date', autocomplete="off"),

            ButtonHolder(
                Submit('submit', 'Submit', css_class="btn btn-success")
            )
        )

        
    class Meta:
        model = Transaction
        fields = (
            'member',
            'previous_month_loan',
            'monthly_saving',
            'interest',
            'fine',
            'others',
            'loan_amount_paid',
            'remaining_loan_amount',
            'additional_loan_amount',
            'total_amount_paid',
            'total_loan_amount',
            'date',
        )

    def clean_loan_amount_paid(self):
        loan_amount_paid = self.cleaned_data.get('loan_amount_paid')
        previous_month_loan = self.cleaned_data.get('previous_month_loan')
        if loan_amount_paid is not None:
            if loan_amount_paid > previous_month_loan:
                raise forms.ValidationError("Loan Amount is not that much high.")
        if previous_month_loan < 0:
            raise forms.ValidationError("No loan amount to be paid.")
        return loan_amount_paid

    def clean_date(self):
        member = self.cleaned_data.get('member')
        np_date_str = self.cleaned_data.get('date')

        date = bs_to_ad(np_date_str)

        np_date = NepaliDate.to_nepali_date(date)
        np_previous_month = get_nepali_prev_month(date)

        previous_month_date = date.replace(day=1) - datetime.timedelta(days=1)

        qs_exists = Transaction.objects.filter(member=member).exists()
        if qs_exists:
            if transaction_month_exists(member, np_date):
                raise forms.ValidationError(
                    "Data already entered for this month."
                )

            qs2 = Transaction.objects.filter(
                member=member,
                date__year=previous_month_date.year,
                date__month=previous_month_date.month
            )
            if not qs2.exists():
                raise forms.ValidationError(
                    "Transaction has not been done on previous month."
                )
        
        return date
