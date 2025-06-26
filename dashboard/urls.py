from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_default'),
    path('<str:country_code>/', views.dashboard_view, name='dashboard_by_country'),
]
