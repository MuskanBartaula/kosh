from django.urls import path

from . import views

app_name = 'loans'

urlpatterns = [
    path('add/', views.add_loan_amount, name="add"),
]
