from django.urls import path

from . import views

app_name = "savings"

urlpatterns = [
    path('', views.monthly_saving, name="monthly_saving"),
    path('add/', views.MonthlySavingCreateView.as_view(), name="add"),
    path('update/<int:pk>/', views.MonthlySavingUpdateView.as_view(), name="update"),
]
