from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from kosh.core.views import (
    transactions_filter_page,
    individual_member_monthly_transaction,
    members_monthly_transaction, export_to_excel
)

urlpatterns = [
    path('', members_monthly_transaction, name="members_monthly_transaction"),
    path('individual/', individual_member_monthly_transaction, name="individual_member_monthly_transaction"),
    path('export/<int:year>/<int:month>/', export_to_excel, name="export_to_excel"),
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
