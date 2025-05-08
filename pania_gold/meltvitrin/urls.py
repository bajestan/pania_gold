from django.urls import path
from . import views



app_name = 'meltvitrin'
urlpatterns = [
        path('meltcart-detail/<str:gold_type>/<int:golditem_id>/', views.meltcart_detail, name='meltcart_detail'),
        path('meltvitrin_list/', views.meltvitrin_list, name='meltvitrin_list'),
        path('add-to-invoice-melt/<str:piece_type>/<int:piece_id>/', views.add_to_invoice_melt, name='add_to_invoice_melt'),
        path('sale-invoice-melt-detail/<int:invoice_id>/', views.sale_invoice_melt_detail, name='sale_invoice_melt_detail'),
        path('create-sale-melt-invoice/', views.create_sale_melt_invoice, name='create_sale_melt_invoice'),
        path('remove-from-invoice-melt/', views.remove_from_invoice_melt, name='remove_from_invoice_melt'),
        path('sale-invoice-melt-list/', views.sale_invoice_melt_list, name='sale_invoice_melt_list'),
        path('sale-meltpiece-list/', views.sale_meltpiece_list, name='sale_meltpiece_list'),




]