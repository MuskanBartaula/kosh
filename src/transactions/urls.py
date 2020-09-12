from django.urls import path

from . import views

app_name = 'transactions'

urlpatterns = [
    path(
        '',
         views.add_member_to_transaction,
         name="add_member_to_transaction"
    ),

    path(
        'create/<int:member_id>/',
         views.TransactionCreateView.as_view(),
         name="create"
    ),
    path(
        'update/<int:pk>/',
        views.TransactionUpdateView.as_view(),
        name="update"
    ),

    path(
        'vouchers/<int:id>/',
        views.transaction_voucher,
        name="vouchers"
    ),

]
