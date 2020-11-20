from django.urls import path

from . import views

app_name = 'members'

urlpatterns = [
    path('', views.MemberCreateView.as_view(), name="index"),
    path('detail/<int:pk>/', views.MemberDetailView.as_view(), name="detail"),
    path('update/<int:pk>/', views.MemberUpdateView.as_view(), name="update"),
    path('delete/<int:pk>/', views.MemberDeleteView.as_view(), name="delete"),
]
