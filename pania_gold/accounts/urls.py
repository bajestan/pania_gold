
from django.urls import path
from . import views



app_name = 'accounts'
urlpatterns = [
        path('', views.home_view, name='home'),
        path('login', views.login_view, name='login'),
        path('logout/', views.user_logout, name='logout'),

        path('melt_view/', views.melt_view, name='melt_view'),
        path('craft_view/', views.craft_view, name='craft_view'),
        path('old_view/', views.old_view, name='old_view'),
        path('scrap_view/', views.scrap_view, name='scrap_view'),
        path('raw_view/', views.raw_view, name='raw_view'),
        path('finance_view/', views.finance_view, name='finance_view'),
        path('report_view/', views.report_view, name='report_view'),
        path('vitrin_view/', views.vitrin_view, name='vitrin_view'),

]
