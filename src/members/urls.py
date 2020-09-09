from django.urls import path

from . import views
app_name = 'members'

urlpatterns = [
    path('', views.MemberCreateView.as_view(), name="index"),
    path('update/<int:pk>/', views.MemberUpdateView.as_view(), name="update"),
    path('delete/<int:pk>/', views.MemberDeleteView.as_view(), name="delete"),
    

    path('monthly-saving/add/', views.MonthlySavingCreateView.as_view(), name="monthly_saving_add"),

]
