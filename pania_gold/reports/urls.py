from django.urls import path
from . import views




app_name = 'reports'
urlpatterns = [

    path('buyraw-diagram-weight-dailyprice/', views.buyraw_diagram_weight_dailyprice, name='buyraw_diagram_weight_dailyprice'),
    path('supply_and_sale_comparison/', views.supply_and_sale_comparison, name='supply_and_sale_comparison'),
]