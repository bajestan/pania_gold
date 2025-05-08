from jdatetime import datetime as jdatetime
import jdatetime
from django.shortcuts import render, get_object_or_404, redirect
from vitrin.models import SaleInvoice,OldPiece
from meltvitrin.models import SaleMeltInvoice
from paniavault.models import BuyRawInvoice
from .forms import SaleInvoicePaymentForm
from .forms import MeltSaleInvoicePaymentForm,BuyrawInvoicePaymentForm,OldPiecePaymentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages





# -----------------------ثبت پرداخت فاکتور فروش زینتی----------------
# تابع بررسی عضویت در گروه
def is_finance_admin(user):
    return user.groups.filter(name="مالی").exists() or user.is_superuser

@login_required
def add_saleinvoice_payment(request, invoice_id):
    if not is_finance_admin(request.user):
        messages.error(request, "شما مجاز به ورود به این صفحه نمی‌باشید")
        return redirect('vitrin:sale_invoice_list')
    invoice = get_object_or_404(SaleInvoice, id=invoice_id)
    if request.method == 'POST':
        payment_form = SaleInvoicePaymentForm(request.POST)
        jalali_date = payment_form.data['pay_date']
        try:
            formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            payment_form.data = payment_form.data.copy()  # داده‌های فرم باید قابل ویرایش باشند
            payment_form.data['pay_date'] = formatted_date
        except ValueError:
            payment_form.add_error('pay_date', 'تاریخ وارد شده نامعتبر است.')

        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.saleinvoice = invoice
            payment.save()
            return redirect('vitrin:sale_invoice_list')

    else:
        payment_form = SaleInvoicePaymentForm()

    return render(request, 'finance/add_saleinvoice_payment.html', {
        'payment_form': payment_form,
        'invoice': invoice,
    })
# -------------------------------------------


# -----------------------ثبت پرداخت فاکتور فروش آبشده----------------
# تابع بررسی عضویت در گروه
def is_finance_admin(user):
    return user.groups.filter(name="مالی").exists() or user.is_superuser

@login_required
def add_meltsale_invoice_payment(request, invoice_id):
    if not is_finance_admin(request.user):
        messages.error(request, "شما مجاز به ورود به این صفحه نمی‌باشید")
        return redirect('meltvitrin:sale_invoice_melt_list')
    invoice = get_object_or_404(SaleMeltInvoice, id=invoice_id)
    if request.method == 'POST':
        payment_form = MeltSaleInvoicePaymentForm(request.POST)
        jalali_date = payment_form.data['pay_date']
        try:
            formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            payment_form.data = payment_form.data.copy()  # داده‌های فرم باید قابل ویرایش باشند
            payment_form.data['pay_date'] = formatted_date
        except ValueError:
            payment_form.add_error('pay_date', 'تاریخ وارد شده نامعتبر است.')

        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.meltsaleinvoice = invoice
            payment.save()
            return redirect('meltvitrin:sale_invoice_melt_list')

    else:
        payment_form = MeltSaleInvoicePaymentForm()

    return render(request, 'finance/add_meltsaleinvoice_payment.html', {
        'payment_form': payment_form,
        'invoice': invoice,
    })

# -----------------------ثبت پرداخت فاکتور تامین خام----------------
# تابع بررسی عضویت در گروه
def is_finance_admin(user):
    return user.groups.filter(name="مالی").exists() or user.is_superuser

@login_required
def add_buyraw_invoice_payment(request, invoice_id):
    if not is_finance_admin(request.user):
        messages.error(request, "شما مجاز به ورود به این صفحه نمی‌باشید")
        return redirect('paniavault:buyraw_invoice_list')
    invoice = get_object_or_404(BuyRawInvoice, id=invoice_id)
    if request.method == 'POST':
        payment_form = BuyrawInvoicePaymentForm(request.POST)
        jalali_date = payment_form.data['pay_date']
        try:
            formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            payment_form.data = payment_form.data.copy()  # داده‌های فرم باید قابل ویرایش باشند
            payment_form.data['pay_date'] = formatted_date
        except ValueError:
            payment_form.add_error('pay_date', 'تاریخ وارد شده نامعتبر است.')

        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.buyrawinvoice = invoice
            payment.save()
            return redirect('paniavault:buyraw_invoice_list')

    else:
        payment_form = BuyrawInvoicePaymentForm()

    return render(request, 'finance/add_buyraw_invoice_payment.html', {
        'payment_form': payment_form,
        'invoice': invoice,
    })


# -----------------------ثبت پرداخت تامین مستعمل----------------
# تابع بررسی عضویت در گروه
def is_finance_admin(user):
    return user.groups.filter(name="مالی").exists() or user.is_superuser

@login_required
def add_buyoldpiece_payment(request, invoice_id):
    if not is_finance_admin(request.user):
        messages.error(request, "شما مجاز به ورود به این صفحه نمی‌باشید")
        return redirect('vitrin:buy_oldpiece_list')
    invoice = get_object_or_404(OldPiece, id=invoice_id)
    if request.method == 'POST':
        payment_form = OldPiecePaymentForm(request.POST)
        jalali_date = payment_form.data['pay_date']
        try:
            formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            payment_form.data = payment_form.data.copy()  # داده‌های فرم باید قابل ویرایش باشند
            payment_form.data['pay_date'] = formatted_date
        except ValueError:
            payment_form.add_error('pay_date', 'تاریخ وارد شده نامعتبر است.')

        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.oldpiece = invoice
            payment.save()
            return redirect('vitrin:buy_oldpiece_list')

    else:
        payment_form = OldPiecePaymentForm()

    return render(request, 'finance/add_buyoldpiece_payment.html', {
        'payment_form': payment_form,
        'invoice': invoice,
    })

# ---------------------------------------------