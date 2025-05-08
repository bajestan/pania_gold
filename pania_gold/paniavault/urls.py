from django.urls import path
from . import views



app_name = 'paniavault'
urlpatterns = [
    path('customer_register/', views.customer_register, name='customer_register'),
    path('supplier_register/', views.supplier_register, name='supplier_register'),


    path('buyraw_invoice_register/', views.buyraw_invoice_register, name='buyraw_invoice_register'),
    path('buyraw_invoice_list/', views.buyraw_invoice_list, name='buyraw_invoice_list'),
    path('buyraw_invoice_detail/<int:invoice_id>/', views.buyraw_invoice_detail, name='buyraw_invoice_detail'),
    path('company_vault_and_vitrin_list/', views.company_vault_and_vitrin_list, name='company_vault_and_vitrin_list'),

    path('buyscrap_invoice_register/', views.buyscrap_invoice_register, name='buyscrap_invoice_register'),
    path('buyscrap_invoice_list/', views.buyscrap_invoice_list, name='buyscrap_invoice_list'),

    path('create_recipt_melt_invoice/', views.create_recipt_melt_invoice, name='create_recipt_melt_invoice'),
    path('register_melt_piece/<int:invoice_id>/', views.register_melt_piece, name='register_melt_piece'),  # مسیر جدید برای ثبت قطعات
    path('recipt_melt_invoice_list/', views.recipt_melt_invoice_list, name='recipt_melt_invoice_list'),

    path('create_recipt_craft_invoice/', views.create_recipt_craft_invoice, name='create_recipt_craft_invoice'),
    path('register_craft_piece/<int:invoice_id>/', views.register_craft_piece, name='register_craft_piece'),
    path('recipt_craft_invoice_list/', views.recipt_craft_invoice_list, name='recipt_craft_invoice_list'),
    path('download-craft-pieces/<int:invoice_id>/', views.download_craft_pieces_excel, name='download_craft_pieces_excel'),

]