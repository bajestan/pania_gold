from django.shortcuts import render
from paniavault.models import BuyRawInvoice,BuyScrapInvoice
from vitrin.models import CraftPiece,OldPiece
import pandas as pd
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, Q
from datetime import datetime
import jdatetime
from decimal import Decimal
from itertools import zip_longest
from decimal import Decimal, InvalidOperation


def buyraw_diagram_weight_dailyprice(request):

    filters = request.session.get('buyraw_diagram_weight_dailyprice', {})

    if request.GET:
        request.session['buyraw_diagram_weight_dailyprice'] = {
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
        }
        filters = request.session['buyraw_diagram_weight_dailyprice']

    # گرفتن تاریخ‌های ورودی از فرم یا سشن
    start_date_str = request.GET.get('start_date') or filters.get('start_date', '')
    end_date_str = request.GET.get('end_date') or filters.get('end_date', '')

    start_date = None
    end_date = None

    if start_date_str:
        try:
            start_date = jdatetime.datetime.strptime(start_date_str, '%Y/%m/%d').date()
        except ValueError:
            pass

    if end_date_str:
        try:
            end_date = jdatetime.datetime.strptime(end_date_str, '%Y/%m/%d').date()
        except ValueError:
            pass

    if not start_date_str and not end_date_str:
        end_date = jdatetime.date.today()
        start_date = jdatetime.date(end_date.year, 1, 1)
    else:

        if start_date and not end_date:
            end_date = jdatetime.date.today()
        elif end_date and not start_date:
            start_date = jdatetime.date(end_date.year, 1, 1)

    #آماده سازی فیلتر تاریخ درصورت وجود داده معتبر
    date_filters = {}
    if isinstance(start_date, jdatetime.date):
        date_filters['invoice_date__gte'] = start_date
    if isinstance(end_date, jdatetime.date):
        date_filters['invoice_date__lte'] = end_date

    # گرفتن دیتا خرید از دیتابیس
    raw_invoices = BuyRawInvoice.objects.filter(**date_filters, supply_type='gallery')
    scrap_invoices = BuyScrapInvoice.objects.filter(**date_filters)
    old_supply = OldPiece.objects.filter(buy_date__range=(start_date, end_date)) if isinstance(start_date,
                                                                                               jdatetime.date) and isinstance(
        end_date, jdatetime.date) else OldPiece.objects.none()

    # تبدیل به دیتا فریم
    df_raw = pd.DataFrame.from_records(raw_invoices.values('invoice_date', 'net_weight', 'invoice_dailyprice'))
    df_scrap = pd.DataFrame.from_records(scrap_invoices.values('invoice_date', 'net_weight', 'invoice_dailyprice'))
    df_old = pd.DataFrame.from_records(old_supply.values('buy_date', 'net_weight', 'buy_dailyprice'))
    df_old.rename(columns={"buy_date": "invoice_date", "buy_dailyprice": "invoice_dailyprice"}, inplace=True)

    # اضافه کردن داده های خرید
    df_purchase = pd.concat([df_raw, df_scrap, df_old], ignore_index=True)

    # گرفتن دیتا فروش از دیتابیس
    craftpieces = CraftPiece.objects.filter(is_sold=True).select_related('sale_invoice')
    oldpieces = OldPiece.objects.filter(is_sold=True).select_related('sale_invoice')

    if isinstance(start_date, jdatetime.date) and isinstance(end_date, jdatetime.date):
        craftpieces = craftpieces.filter(sale_invoice__sale_date__range=(start_date, end_date))
        oldpieces = oldpieces.filter(sale_invoice__sale_date__range=(start_date, end_date))

    df_craft = pd.DataFrame.from_records(
        craftpieces.values('sale_invoice__sale_date', 'net_weight', 'sale_invoice__sale_dailyprice'))
    df_old_sale = pd.DataFrame.from_records(
        oldpieces.values('sale_invoice__sale_date', 'net_weight', 'sale_invoice__sale_dailyprice'))
    df_sale = pd.concat([df_craft, df_old_sale], ignore_index=True)

    # آماده‌سازی داده‌های خرید
    purchase_data = {'labels': [], 'data': []}
    if not df_purchase.empty:
        df_purchase['invoice_date'] = df_purchase['invoice_date'].apply(
            lambda d: d.strftime('%Y/%m/%d') if not isinstance(d, str) else d)
        df_purchase['net_weight'] = df_purchase['net_weight'].astype(float)
        df_purchase['invoice_dailyprice'] = df_purchase['invoice_dailyprice'].astype(float)
        df_purchase['weighted_price'] = df_purchase['net_weight'] * df_purchase['invoice_dailyprice']
        purchase_grouped = df_purchase.groupby('invoice_date').agg({'net_weight': 'sum', 'weighted_price': 'sum'})
        purchase_grouped['avg_price'] = purchase_grouped['weighted_price'] / purchase_grouped['net_weight']
        purchase_grouped = purchase_grouped.reset_index()
        purchase_data = {
            'labels': purchase_grouped['invoice_date'].tolist(),
            'data': purchase_grouped['avg_price'].round(2).tolist(),
        }

    # آماده‌سازی داده‌های فروش
    sale_data = {'labels': [], 'data': []}
    if not df_sale.empty:
        df_sale['sale_invoice__sale_date'] = df_sale['sale_invoice__sale_date'].apply(
            lambda d: d.strftime('%Y/%m/%d') if not isinstance(d, str) else d)
        df_sale['net_weight'] = df_sale['net_weight'].astype(float)
        df_sale['sale_invoice__sale_dailyprice'] = df_sale['sale_invoice__sale_dailyprice'].astype(float)
        df_sale['weighted_price'] = df_sale['net_weight'] * df_sale['sale_invoice__sale_dailyprice']
        sale_grouped = df_sale.groupby('sale_invoice__sale_date').agg({'net_weight': 'sum', 'weighted_price': 'sum'})
        sale_grouped['avg_price'] = sale_grouped['weighted_price'] / sale_grouped['net_weight']
        sale_grouped = sale_grouped.reset_index()
        sale_data = {
            'labels': sale_grouped['sale_invoice__sale_date'].tolist(),
            'data': sale_grouped['avg_price'].round(2).tolist(),
        }

    # آماده سازی کل داده ها
    context = {
        'purchase_data': purchase_data,
        'sale_data': sale_data,
        'start_date': start_date_str if not isinstance(start_date, jdatetime.date) else start_date.strftime('%Y/%m/%d'),
        'end_date': end_date_str if not isinstance(end_date, jdatetime.date) else end_date.strftime('%Y/%m/%d'),
    }

    return render(request, 'reports/buyraw_diagram_weight_dailyprice.html', context)


# -------------------------------------------


@login_required
def supply_and_sale_comparison(request):
    if request.GET:
        request.session['supply_and_sale_comparison_filters'] = {
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
        }

    filters = request.session.get('supply_and_sale_comparison_filters', {})
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')
    start_date_jalali = end_date_jalali = ''
    start_date_gregorian = end_date_gregorian = None

    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()
        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y/%m/%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y/%m/%d')

    # --- خرید از خام فقط مخصوص گالری ---
    buyraw = BuyRawInvoice.objects.filter(supply_type='gallery')

    if start_date_gregorian and end_date_gregorian:
        buyraw = buyraw.filter(invoice_date__range=(start_date_gregorian, end_date_gregorian))
    else:
        buyraw = buyraw.order_by('-invoice_date')[:5]

    raw_data = [{
        'date': invoice.invoice_date,
        'weight': invoice.net_weight,
        'price': invoice.invoice_price,
        'dailyprice': invoice.invoice_dailyprice,
        'type': f"خام -{dict(BuyRawInvoice.SUPPLY_TYPE_CHOICES).get(invoice.supply_type, '')}",
    } for invoice in buyraw]

    # --- خرید از قیچی ---
    buyscrap = BuyScrapInvoice.objects.all()

    if start_date_gregorian and end_date_gregorian:
        buyscrap = buyscrap.filter(invoice_date__range=(start_date_gregorian, end_date_gregorian))
    else:
        buyscrap = buyscrap.order_by('-invoice_date')[:5]

    scrap_data = [{
        'date': invoice.invoice_date,
        'weight': invoice.net_weight,
        'price': invoice.invoice_price,
        'dailyprice': invoice.invoice_dailyprice,
        'type': 'قیچی',
    } for invoice in buyscrap]

    # ----------- تأمین از مستعمل -------------
    oldpieces_supply = OldPiece.objects.all()

    if start_date_gregorian and end_date_gregorian:
        oldpieces_supply = oldpieces_supply.filter(
            buy_date__range=(start_date_gregorian, end_date_gregorian)
        )
    else:
        oldpieces_supply = oldpieces_supply.order_by('-buy_date')[:5]

    oldpiece_data = [{
        'date': piece.buy_date,
        'weight': piece.net_weight,
        'price': piece.buy_price,
        'dailyprice': piece.buy_dailyprice,
        'type': 'مستعمل',
    } for piece in oldpieces_supply]

    # --- فروش ---
    craftpieces = CraftPiece.objects.filter(is_sold=True).select_related('sale_invoice')
    oldpieces = OldPiece.objects.filter(is_sold=True).select_related('sale_invoice')

    if start_date_gregorian and end_date_gregorian:
        craftpieces = craftpieces.filter(sale_invoice__sale_date__range=(start_date_gregorian, end_date_gregorian))
        oldpieces = oldpieces.filter(sale_invoice__sale_date__range=(start_date_gregorian, end_date_gregorian))
    else:
        craftpieces = craftpieces.order_by('-sale_date')[:5]
        oldpieces = oldpieces.order_by('-sale_date')[:5]

    sale_data = []
    for piece in list(craftpieces) + list(oldpieces):
        date = piece.sale_invoice.sale_date if piece.sale_invoice else piece.created_at
        sale_data.append({
            'date': date,
            'weight': piece.net_weight,
            'price': piece.sale_price,
            'dailyprice': piece.sale_invoice.sale_dailyprice if piece.sale_invoice else None,
            'type': 'craft' if isinstance(piece, CraftPiece) else 'old',
        })

    # --- محاسبه مجموع وزن و میانگین وزنی نرخ روز برای فروش ---
    total_sale_weight = Decimal('0.00')
    weighted_sale_dailyprice_sum = Decimal('0.00')
    for item in sale_data:
        try:
            weight = Decimal(item['weight']) if item['weight'] else Decimal('0.00')
            dailyprice = Decimal(item['dailyprice']) if item['dailyprice'] else None
            total_sale_weight += weight
            if dailyprice:
                weighted_sale_dailyprice_sum += weight * dailyprice
        except InvalidOperation:
            continue

    avg_sale_dailyprice = int((weighted_sale_dailyprice_sum / total_sale_weight).quantize(Decimal('0.01'))) if total_sale_weight > 0 else 0

    # --- محاسبه مجموع وزن و میانگین وزنی نرخ روز برای تأمین ---
    supply_data = raw_data + scrap_data + oldpiece_data

    sale_data.sort(key=lambda x: x['date'], reverse=True)
    supply_data.sort(key=lambda x: x['date'], reverse=True)

    total_supply_weight = Decimal('0.00')
    weighted_supply_dailyprice_sum = Decimal('0.00')
    for item in supply_data:
        try:
            weight = Decimal(item['weight']) if item['weight'] else Decimal('0.00')
            dailyprice = Decimal(item['dailyprice']) if item['dailyprice'] else None
            total_supply_weight += weight
            if dailyprice:
                weighted_supply_dailyprice_sum += weight * dailyprice
        except InvalidOperation:
            continue

    avg_supply_dailyprice = int((weighted_supply_dailyprice_sum / total_supply_weight).quantize(Decimal('0.01'))) if total_supply_weight > 0 else 0

    context = {
        'filters': filters,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'supply_data': supply_data,
        'sale_data': sale_data,
        'total_sale_weight': total_sale_weight,
        'avg_sale_dailyprice': avg_sale_dailyprice,
        'total_supply_weight': total_supply_weight,
        'avg_supply_dailyprice': avg_supply_dailyprice,
        'combined_data': zip_longest(sale_data, supply_data),
    }

    return render(request, 'reports/supply_and_sale_comparison.html', context)
