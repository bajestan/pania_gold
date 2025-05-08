from django.urls import path
from . import views



app_name = 'finance'
urlpatterns = [
        path('add_saleinvoice_payment/<int:invoice_id>/', views.add_saleinvoice_payment, name='add_saleinvoice_payment'),
        path('add_meltsale_invoice_payment/<int:invoice_id>/', views.add_meltsale_invoice_payment, name='add_meltsale_invoice_payment'),
        path('add_buyraw_invoice_payment/<int:invoice_id>/', views.add_buyraw_invoice_payment, name='add_buyraw_invoice_payment'),
        path('add_buyoldpiece_payment/<int:invoice_id>/', views.add_buyoldpiece_payment, name='add_buyoldpiece_payment'),





]