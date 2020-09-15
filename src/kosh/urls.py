from django.contrib import admin
from django.urls import path, include

from .views import members_monthly_transaction, export_to_excel

urlpatterns = [
    path('', members_monthly_transaction, name="members_monthly_transaction"),
    path('export/<int:year>/<int:month>/', export_to_excel, name="export_to_excel"),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('loans/', include('loans.urls')),
    path('members/', include('members.urls')),
    path('transactions/', include('transactions.urls')),
]
