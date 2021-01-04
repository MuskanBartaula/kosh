from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from kosh.core.views import (
    individual_member_monthly_transaction,
    members_monthly_transaction, export_to_excel,
    individual_transaction_to_excel
)

urlpatterns = [
    path(
        '',
        members_monthly_transaction,
        name="members_monthly_transaction"
    ),
    path(
        'individual/',
        individual_member_monthly_transaction,
        name="individual_member_monthly_transaction"
    ),
    path(
        'export/<int:year>/<int:month>/<int:day>/',
        export_to_excel, name="export_to_excel"
    ),
    path(
        'individual-member-transaction-to-excel/<int:member_id>/<str:start_date>/<str:end_date>',
        individual_transaction_to_excel,
        name="individual_transaction_to_excel"),
    path('admin/', admin.site.urls),
    path('accounts/', include('kosh.accounts.urls')),
    path('members/', include('kosh.members.urls')),
    path('monthly_saving/', include('kosh.savings.urls')),
    path('transactions/', include('kosh.transactions.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
