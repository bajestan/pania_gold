from django.urls import path
from . import views



app_name = 'vitrin'
urlpatterns = [
        path('vitrin_list/', views.vitrin_list, name='vitrin_list'),
        path('cart-detail/<str:gold_type>/<int:golditem_id>/', views.cart_detail, name='cart_detail'),

        path('register_old_piece/', views.register_old_piece, name='register_old_piece'),
        path('buy_oldpiece_list/', views.buy_oldpiece_list, name='buy_oldpiece_list'),

        path('add-to-invoice/<str:piece_type>/<int:piece_id>/', views.add_to_invoice, name='add_to_invoice'),
        path('sale-invoice-detail/<int:invoice_id>/', views.sale_invoice_detail, name='sale_invoice_detail'),
        path('create-sale-invoice/', views.create_sale_invoice, name='create_sale_invoice'),
        path('remove-from-invoice/', views.remove_from_invoice, name='remove_from_invoice'),
        path('sale-invoice-list/', views.sale_invoice_list, name='sale_invoice_list'),
        path('sale-piece-list/', views.sale_piece_list, name='sale_piece_list'),
        path('buy_oldpiece_detail/<int:invoice_id>/', views.buy_oldpiece_detail, name='buy_oldpiece_detail'),

        path('checklist_vitrin_craft_old/', views.checklist_vitrin_craft_old, name='checklist_vitrin_craft_old'),



]