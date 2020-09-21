import datetime
import xlwt

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from nepali_date import NepaliDate

from kosh.utils import split_date, bs_to_ad, NepaliDateUtils
from members.models import Member
from transactions.forms import TransactionDateFilterForm
from transactions.models import Transaction

@login_required
def members_monthly_transaction(request):
    date_in_bs = request.GET.get('date')

    form = TransactionDateFilterForm()
    transaction_date = timezone.now().date()

    if date_in_bs:
        data = {'date': date_in_bs}
        form = TransactionDateFilterForm(data)
        if form.is_valid():
            np_date_str = form.cleaned_data.get('date')
            transaction_date = bs_to_ad(np_date_str)

    np_date_utils = NepaliDateUtils(transaction_date)
    start_date, end_date = np_date_utils.start_end_date_in_ad()
    members = Member.objects.all().order_by('membership_id')
    transactions = Transaction.objects.filter(date__range=(start_date, end_date))

    context = {
        'form': form,
        'transaction_date': transaction_date,
        'members': members,
        'transactions': transactions,
    }

    return render(request, "transactions/members_monthly_transaction.html", context)

@login_required
def export_to_excel(request, year, month):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="kosh.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Transactions')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        'S.N.',
        'Name',
        'Number of Share',
        'Previous Month Loan',
        'Monthly Saving',
        'Loan Amount Paid',
        'Interest',
        'Fine',
        'Others',
        'Total Amount Paid',
        'Remaining Loan Amount',
        'Additional Loan Amount',
        'Total Loan Amount',
    ]

    for col_num, column in enumerate(columns):
        ws.write(row_num, col_num, column, font_style)

    font_style = xlwt.XFStyle()

    transactions = Transaction.objects.filter(date__year=year,
                                              date__month=month)
    members = Member.objects.all().order_by('membership_id')

    for member in members:
        row_num += 1
        ws.write(row_num, 0, member.membership_id, font_style)
        ws.write(row_num, 1, member.name, font_style)
        ws.write(row_num, 2, member.number_of_share, font_style)
        for transaction in transactions:
            if member.membership_id == transaction.member.membership_id:
                ws.write(row_num, 3, transaction.previous_month_loan, font_style)
                ws.write(row_num, 4, transaction.monthly_saving, font_style)
                ws.write(row_num, 5, transaction.loan_amount_paid, font_style)
                ws.write(row_num, 6, transaction.interest, font_style)
                ws.write(row_num, 7, transaction.fine, font_style)
                ws.write(row_num, 8, transaction.others, font_style)
                ws.write(row_num, 9, transaction.total_amount_paid, font_style)
                ws.write(row_num, 10, transaction.remaining_loan_amount, font_style)
                ws.write(row_num, 11, transaction.additional_loan_amount, font_style)
                ws.write(row_num, 12, transaction.total_loan_amount, font_style)

    wb.save(response)
    return response
