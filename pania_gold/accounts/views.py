from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from .models import HomeImage





@login_required
def home_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'buyraw_invoice_register': reverse('paniavault:buyraw_invoice_register'),
        'buyscrap_invoice_register': reverse('paniavault:buyscrap_invoice_register'),
        'create_recipt_melt_invoice': reverse('paniavault:create_recipt_melt_invoice'),
        'create_recipt_craft_invoice': reverse('paniavault:create_recipt_craft_invoice'),
        'register_old_piece': reverse('vitrin:register_old_piece'),

        'melt_view': reverse('accounts:melt_view'),
        'craft_view': reverse('accounts:craft_view'),
        'old_view': reverse('accounts:old_view'),
        'scrap_view': reverse('accounts:scrap_view'),
        'raw_view': reverse('accounts:raw_view'),
        'finance_view': reverse('accounts:finance_view'),
        'report_view': reverse('accounts:report_view'),
        'vitrin_view': reverse('accounts:vitrin_view'),

        'images': {
            'buyraw_invoice_register': 'media/home_images/rawgold.png',
            'buyscrap_invoice_register': 'media/home_images/scrapgold.png',
            'create_recipt_melt_invoice': 'media/home_images/meltgold.png',
            'create_recipt_craft_invoice': 'media/home_images/craftgold.png',
            'register_old_piece': 'media/home_images/oldgold.png',
            'finance_view':'media/home_images/finance.png',
            'report_view': 'media/home_images/report.png',
            'vitrin_view': 'media/home_images/vitrin.png',

        },
    }
    return render(request, 'accounts/home.html', context)
# ----------------------------------------------------

@login_required
def melt_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'create_recipt_melt_invoice': reverse('paniavault:create_recipt_melt_invoice'),
        'recipt_melt_invoice_list': reverse('paniavault:recipt_melt_invoice_list'),
        'sale_invoice_melt_list': reverse('meltvitrin:sale_invoice_melt_list'),
        'sale_meltpiece_list': reverse('meltvitrin:sale_meltpiece_list'),
    }
    return render(request, 'accounts/melt_view.html', context)

# -----------------------------------------------
@login_required
def craft_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'create_recipt_craft_invoice': reverse('paniavault:create_recipt_craft_invoice'),
        'recipt_craft_invoice_list': reverse('paniavault:recipt_craft_invoice_list'),
        'sale_craftinvoice_list': reverse('vitrin:sale_invoice_list'),
        'sale_craftpiece_list': reverse('vitrin:sale_piece_list'),
    }

    return render(request, 'accounts/craft_view.html', context)
# ----------------------------------------
@login_required
def old_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'register_old_piece': reverse('vitrin:register_old_piece'),
        'buy_oldpiece_list': reverse('vitrin:buy_oldpiece_list'),
        # 'sale_oldpiece_list': reverse('vitrin:sale_oldpiece_list'),
    }

    return render(request, 'accounts/old_view.html', context)
# --------------------------------------

@login_required
def scrap_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'buyscrap_invoice_register': reverse('paniavault:buyscrap_invoice_register'),
        'buyscrap_invoice_list': reverse('paniavault:buyscrap_invoice_list'),
    }

    return render(request, 'accounts/scrap_view.html', context)
# ---------------------------------------
@login_required
def raw_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'buyraw_invoice_register': reverse('paniavault:buyraw_invoice_register'),
        'buyraw_invoice_list': reverse('paniavault:buyraw_invoice_list'),
    }

    return render(request, 'accounts/raw_view.html', context)
# ------------------------------------
@login_required
def finance_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'create_recipt_craft_invoice': reverse('paniavault:create_recipt_craft_invoice'),

    }
    return render(request, 'accounts/finance_view.html', context)
# ------------------------------------------
@login_required
def report_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'buyraw_diagram_weight_dailyprice': reverse('reports:buyraw_diagram_weight_dailyprice'),
        'supply_and_sale_comparison': reverse('reports:supply_and_sale_comparison'),

    }
    return render(request, 'accounts/report_view.html', context)
# ----------------------------------------
@login_required
def vitrin_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'vitrin_list': reverse('vitrin:vitrin_list'),
        'checklist_vitrin': reverse('vitrin:checklist_vitrin_craft_old'),
    }

    return render(request, 'accounts/vitrin_view.html', context)
# --------------------------------
def user_logout(request):
    logout(request)
    return redirect('accounts:login')  # بعد از لاگ‌اوت به صفحه لاگین هدایت می‌شود


def login_view(request):
    try:
        login_image = HomeImage.objects.get(description='login')
    except HomeImage.DoesNotExist:
        login_image = None
    if request.method == 'POST':
        user_id = request.POST['user_id']
        pass_code = request.POST['pass_code']
        user = authenticate(request, username=user_id, password=pass_code)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')  # هدایت به صفحه demand بعد از ورود موفق
        else:
            messages.error(request, 'رمز عبور یا نام کاربری صحیح نیست')
    context = {
        'login_image': login_image,
    }
    return render(request, 'accounts/login.html',context)

# ------------------------------------
