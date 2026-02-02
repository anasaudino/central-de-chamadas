from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('chamados/', views.ticket_list, name='ticket_list'),
    path('chamados/novo/', views.ticket_create, name='ticket_create'),
    path('chamados/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('chamados/<int:ticket_id>/updates/', views.ticket_updates, name='ticket_updates'),
]
