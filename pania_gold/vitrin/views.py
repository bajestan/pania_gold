
from .models import CraftPiece,OldPiece,CompanyVitrin,SaleInvoice
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404, redirect
from .forms import OldPieceForm,UploadImageForm,SaleInvoiceForm
import time
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import F, Sum, ExpressionWrapper, DecimalField, Q
from .models import CompanyVitrin, OldPiece
from finance.models import OldPiecePayment
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from django.db.models.functions import Coalesce
from decimal import Decimal
import jdatetime
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required





# ========================= old مستعمل ========================



@login_required
def register_old_piece(request):
    vitrin, _ = CompanyVitrin.objects.get_or_create(
        defaults={'vitrin_balance': Decimal('0.00'), 'vitrin_assets': Decimal('0.00')}
    )
    if request.method == 'POST':
        form = OldPieceForm(request.POST, request.FILES)
        jalali_date = request.POST.get('buy_date')
        if jalali_date:
            try:
                formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
                form.data = form.data.copy()
                form.data['buy_date'] = formatted_date
            except ValueError:
                form.add_error('buy_date', 'تاریخ وارد شده نامعتبر است.')
        if form.is_valid():
            supplier = form.cleaned_data.get('supplier')
            net_weight = form.cleaned_data.get('net_weight')
            buy_date = form.cleaned_data.get('buy_date')
            code = form.cleaned_data.get('code')

            existing_piece = OldPiece.objects.filter(
                supplier=supplier,
                net_weight=net_weight,
                buy_date=buy_date
            ).exists()
            if existing_piece:
                form.add_error(None, 'این رکورد قبلاً ثبت شده است')
                return render(request, 'vitrin/register_old_piece.html', {'form': form})

            if not code:
                if net_weight:
                    int_part = int(net_weight)
                    dec_part = int((net_weight - int_part) * 100)
                    formatted_weight = f"{int_part:02d}{dec_part:02d}"
                else:
                    formatted_weight = "0000"

                timestamp = int(time.time())
                last_three_digits = str(timestamp)[-2:]
                generated_code = f"OL{last_three_digits}-{formatted_weight}"
                form.instance.code = generated_code
            else:
                form.instance.code = code

            piece = form.save(commit=False)
            piece.vitrin = vitrin
            piece.save()
            return redirect('vitrin:buy_oldpiece_list')
    else:
        form = OldPieceForm()
    return render(request, 'vitrin/register_old_piece.html', {'form': form})

# -----------------------------------

@login_required
def buy_oldpiece_list(request):
    if request.GET:
        request.session['supply_filters'] = {
            'supply': request.GET.get('supply', ''),
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
        }

    filters = request.session.get('supply_filters', {})
    supply_name = filters.get('supply', '')
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')

    invoices = OldPiece.objects.all()
    start_date_jalali = ''
    end_date_jalali = ''

    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()
        invoices = invoices.filter(buy_date__range=(start_date_gregorian, end_date_gregorian))
        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y/%m/%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y/%m/%d')

    if supply_name:
        invoices = invoices.filter(
            Q(supplier__first_name__icontains=supply_name) |
            Q(supplier__last_name__icontains=supply_name)
        )

    invoices = invoices.order_by('-buy_date')
    if not (start_date or end_date or supply_name):
        invoices = invoices[:10]

    # محاسبه مجموع وزن و مبلغ
    total_weight = invoices.aggregate(total_weight=Sum('net_weight'))['total_weight'] or 0
    total_price = invoices.aggregate(total_price=Sum('buy_price'))['total_price'] or 0

    # محاسبه میانگین وزنی قیمت روز طلا
    weighted_expression = ExpressionWrapper(F('buy_dailyprice') * F('net_weight'), output_field=DecimalField())
    weighted_price_sum = invoices.aggregate(weighted_price=Sum(weighted_expression))['weighted_price'] or 0

    if total_weight and weighted_price_sum:
        weighted_avg_daily_price = int(weighted_price_sum / total_weight)
    else:
        weighted_avg_daily_price = 0

    invoices = invoices.annotate(
        total_paid=Coalesce(Sum('oldpiecepayments__amount'), 0)
    ).annotate(
        remaining=ExpressionWrapper(
            F('total_paid') - F('buy_price'),
            output_field=IntegerField()
        )
    )
    total_remaining = sum(invoice.remaining for invoice in invoices)
    context = {
        'invoices': invoices,
        'supply_name': supply_name,
        'filters': filters,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'total_weight': total_weight,
        'total_price': total_price,
        'weighted_avg_daily_price': weighted_avg_daily_price,
        'total_remaining':total_remaining,
    }
    return render(request, 'vitrin/buy_oldpiece_list.html', context)

# ----------------------------------
@login_required
def buy_oldpiece_detail(request, invoice_id):
    invoice = get_object_or_404(OldPiece, pk=invoice_id)
    payments = invoice.oldpiecepayments.all()  # استفاده از related_name
    total_paid = sum(item.amount for item in payments)
    context = {
        'invoice': invoice,
        'payments': payments,
        'total_paid':total_paid,
    }
    return render(request, 'vitrin/buy_oldpiece_detail.html', context)


# ==========================CRAFT AND OLD VITRIN =======================


@login_required
def vitrin_list(request):
    if request.GET:
        request.session['vitrin_filters'] = {
            'name': request.GET.get('name', ''),
            'code': request.GET.get('code', ''),
            'gold_type': request.GET.getlist('gold_type', [])  # دریافت نوع طلا از درخواست
        }
    filters = request.session.get('vitrin_filters', {})
    name = filters.get('name', '')
    code = filters.get('code', '')
    gold_type = filters.get('gold_type', [])

    craftpieces = CraftPiece.objects.filter(is_sold=False).select_related('sale_invoice__customer', 'supplier')
    oldpieces = OldPiece.objects.filter(is_sold=False).select_related('sale_invoice__customer', 'supplier')

    query_filter = Q()
    if name:
        query_filter |= Q(name__icontains=name) | Q(code__icontains=name)
    if code:
        query_filter |= Q(code__icontains=code)
    craftpieces = craftpieces.filter(query_filter)
    oldpieces = oldpieces.filter(query_filter)

    # فیلتر بر اساس نوع طلا
    selected_pieces = []
    if 'craft' in gold_type:
        selected_pieces.extend(craftpieces)
    if 'old' in gold_type:
        selected_pieces.extend(oldpieces)

    # اگر هیچ فیلتر نوع انتخاب نشده باشد، همه موارد نمایش داده شوند
    if not gold_type:
        selected_pieces = list(craftpieces) + list(oldpieces)

    combined_golds = sorted(selected_pieces, key=lambda x: x.created_at, reverse=True)
    # صفحه‌بندی
    paginator = Paginator(combined_golds, 20)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    # اضافه کردن نوع به قطعات
    pieces = [
        {'piece': piece, 'type': (
            'craft' if isinstance(piece, CraftPiece) else
            'old'
        )}
        for piece in page_obj
    ]
    # دریافت تعداد کالاهای موجود در سبد خرید
    cart = request.session.get('sale_cart', [])
    cart_count = len(cart)  # شمارش تعداد کالاها در سبد خرید

    # محاسبه مجموع وزن و تعداد قطعات
    total_weight = sum([piece.net_weight or 0 for piece in selected_pieces])
    total_count = len(selected_pieces)
    # محاسبه مجموع اجرت برای قطعات زینتی (CraftPiece)
    total_craft_ojrat_weight = sum([
        (Decimal(piece.buy_ojrat or 0) / Decimal(100)) * (piece.net_weight or Decimal(0))
        for piece in selected_pieces
        if isinstance(piece, CraftPiece)
    ])

    context = {
        'page_obj': page_obj,
        'name': name,
        'code': code,
        'filters': filters,
        'gold_type': gold_type,  # ارسال فیلتر به قالب
        'pieces': pieces,
        'cart_count': cart_count,  # ارسال تعداد کالاها به قالب
        'total_weight': total_weight,
        'total_count': total_count,
        'total_craft_ojrat_weight': total_craft_ojrat_weight,
    }
    return render(request, 'vitrin/vitrin_list.html', context)


# --------------------------------

@login_required
def upload_image(request, golditem_id):
    form = UploadImageForm()
    gold_item = None
    models = [ CraftPiece, OldPiece]
    for model in models:
        try:
            gold_item = model.objects.get(id=golditem_id)
            break
        except model.DoesNotExist:
            continue
    if not gold_item:
        return render(request, 'vitrin/cart_detail_not_found.html')
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            gold_item.image = form.cleaned_data['image']
            gold_item.save()
            messages.success(request, "تصویر با موفقیت آپلود شد")
            return redirect('vitrin:cart_detail', golditem_id=golditem_id)
        else:
            messages.error(request, "خطا در آپلود تصویر. لطفاً مجدداً تلاش کنید.")
    return render(request, 'vitrin/cart_detail.html', {'vitrin': gold_item, 'form': form})

# --------------------------------------


@login_required
def cart_detail(request, gold_type, golditem_id):
    vitrin = None
    form = UploadImageForm()

    if gold_type == "old":
        try:
            vitrin = OldPiece.objects.get(id=golditem_id)
        except OldPiece.DoesNotExist:
            return render(request, 'vitrin/cart_detail_not_found.html')
    elif gold_type == "craft":
        try:
            vitrin = CraftPiece.objects.get(id=golditem_id)
        except CraftPiece.DoesNotExist:
            return render(request, 'vitrin/cart_detail_not_found.html')


    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            vitrin.image = form.cleaned_data['image']
            vitrin.save()
            messages.success(request, "تصویر با موفقیت آپلود شد.")
            return redirect('vitrin:cart_detail', gold_type=gold_type, golditem_id=golditem_id)
        else:
            messages.error(request, "خطا در آپلود تصویر. لطفاً مجدداً تلاش کنید.")

    return render(request, 'vitrin/cart_detail.html', {'vitrin': vitrin, 'form': form})
# ====================== انبارگردانی ویترین =====================


@login_required
def checklist_vitrin_craft_old(request):
    if request.GET:
        request.session['checklist_vitrin_filters'] = {
            'name': request.GET.get('name', ''),
            'code': request.GET.get('code', ''),
            'gold_type': request.GET.getlist('gold_type', [])  # دریافت نوع طلا از درخواست
        }
    filters = request.session.get('checklist_vitrin_filters', {})
    name = filters.get('name', '')
    code = filters.get('code', '')
    gold_type = filters.get('gold_type', [])

    craftpieces = CraftPiece.objects.filter(is_sold=False).select_related('sale_invoice__customer', 'supplier')
    oldpieces = OldPiece.objects.filter(is_sold=False).select_related('sale_invoice__customer', 'supplier')

    query_filter = Q()
    if name:
        query_filter |= Q(name__icontains=name) | Q(code__icontains=name)
    if code:
        query_filter |= Q(code__icontains=code)
    craftpieces = craftpieces.filter(query_filter)
    oldpieces = oldpieces.filter(query_filter)

    # فیلتر بر اساس نوع طلا
    selected_pieces = []
    if 'craft' in gold_type:
        selected_pieces.extend(craftpieces)
    if 'old' in gold_type:
        selected_pieces.extend(oldpieces)

    # اگر هیچ فیلتر نوع انتخاب نشده باشد، همه موارد نمایش داده شوند
    if not gold_type:
        selected_pieces = list(craftpieces) + list(oldpieces)


    # دریافت تعداد کالاهای موجود در سبد خرید
    cart = request.session.get('sale_cart', [])
    cart_count = len(cart)  # شمارش تعداد کالاها در سبد خرید

    # محاسبه مجموع وزن و تعداد قطعات
    total_weight = sum([piece.net_weight or 0 for piece in selected_pieces])
    total_count = len(selected_pieces)
    # محاسبه مجموع اجرت برای قطعات زینتی (CraftPiece)
    total_craft_ojrat_weight = sum([
        (Decimal(piece.buy_ojrat or 0) / Decimal(100)) * (piece.net_weight or Decimal(0))
        for piece in selected_pieces
        if isinstance(piece, CraftPiece)
    ])

    context = {
        'name': name,
        'code': code,
        'filters': filters,
        'gold_type': gold_type,  # ارسال فیلتر به قالب
        'cart_count': cart_count,  # ارسال تعداد کالاها به قالب
        'total_weight': total_weight,
        'total_count': total_count,
        'total_craft_ojrat_weight': total_craft_ojrat_weight,
        'selected_pieces': selected_pieces,

    }
    return render(request, 'vitrin/checklist_vitrin_craft_old.html', context)


# ====================  ایجاد فاکتور فروش =====================

# اضافه کردن کالا به سبد خرید
@login_required
def add_to_invoice(request, piece_type, piece_id):
    cart = request.session.get('sale_cart', [])
    if piece_type == 'craft':
        piece = CraftPiece.objects.get(id=piece_id)
    elif piece_type == 'old':
        piece = OldPiece.objects.get(id=piece_id)
    else:
        return redirect('vitrin:vitrin_list')
    cart.append({
        'type': piece_type,  # نوع قطعه (craft یا old)
        'id': piece_id,
        'name': piece.name,
        'net_weight': float(piece.net_weight),
        'code': piece.code,
        'sale_ojrat': float(piece.sale_ojrat or 0),
        'sale_price_ojrat': int(getattr(piece, 'sale_price_ojrat', 0) or 0),
        'image': piece.image.url if piece.image else None,
    })
    request.session['sale_cart'] = cart
    piece.is_sold = True
    piece.save()
    cart_count = len(cart)  # شمارش تعداد کالاها در سبد خرید
    return JsonResponse({'success': True, 'cart_count': cart_count})

# -------------------------------------------
@login_required
def remove_from_invoice(request):
    if request.method == 'POST':
        piece_id = request.POST.get('piece_id')
        piece_type = request.POST.get('piece_type')
        if not piece_id or not piece_type:
            messages.error(request, 'اطلاعات مورد نیاز کامل نیست.')
            return redirect('vitrin:create_sale_invoice')
        try:
            piece_id = int(piece_id)
        except (ValueError, TypeError):
            messages.error(request, 'آیدی کالا معتبر نیست.')
            return redirect('vitrin:create_sale_invoice')

        cart = request.session.get('sale_cart', [])
        cart = [item for item in cart if not (item['id'] == piece_id and item['type'] == piece_type)]
        request.session['sale_cart'] = cart
        if piece_type == 'craft':
            try:
                piece = CraftPiece.objects.get(id=piece_id)
            except CraftPiece.DoesNotExist:
                messages.error(request, 'کالای مورد نظر یافت نشد.')
                return redirect('vitrin:create_sale_invoice')
        else:
            try:
                piece = OldPiece.objects.get(id=piece_id)
            except OldPiece.DoesNotExist:
                messages.error(request, 'کالای مورد نظر یافت نشد.')
                return redirect('vitrin:create_sale_invoice')

        piece.is_sold = False
        piece.save()
        messages.success(request, 'کالا از سبد حذف شد.')
        return redirect('vitrin:create_sale_invoice')
    else:
        return redirect('vitrin:create_sale_invoice')



# -------------------------ایجاد فاکتور فروش----------------


@login_required
def create_sale_invoice(request):
    if request.method == 'POST':
        form = SaleInvoiceForm(request.POST)
        jalali_date = request.POST.get('sale_date')
        if jalali_date:
            try:
                formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
                form.data = form.data.copy()  # کپی کردن داده‌های فرم
                form.data['sale_date'] = formatted_date  # تغییر تاریخ در داده‌ها
            except ValueError:
                messages.error(request, 'تاریخ وارد شده نامعتبر است')
                return render(request, 'vitrin/create_sale_invoice.html', {'form': form})

        sale_dailyprice = request.POST.get('sale_dailyprice')

        if sale_dailyprice:
            form.data = form.data.copy()  # کپی کردن داده‌های فرم
            form.data['sale_dailyprice'] = sale_dailyprice  # تغییر قیمت روزانه در داده‌ها

        # بررسی خالی نبودن سبد خرید قبل از ذخیره فاکتور
        cart = request.session.get('sale_cart', [])
        if not cart:
            messages.error(request, 'سبد خرید خالی است. ابتدا کالا اضافه کنید.')
            return render(request, 'vitrin/create_sale_invoice.html', {'form': form})

        if form.is_valid():
            sale_dailyprice = form.cleaned_data.get('sale_dailyprice')
            customer = form.cleaned_data.get('customer')
            companyseller = form.cleaned_data.get('companyseller')
            sale_date = form.cleaned_data.get('sale_date')
            sale_price = form.cleaned_data.get('sale_price')
            net_sale_price = form.cleaned_data.get('net_sale_price')
            discount = form.cleaned_data.get('discount')
            notes = form.cleaned_data.get('notes')
            invoice_serial = form.cleaned_data.get('invoice_serial')

            invoice = SaleInvoice(
                sale_dailyprice=sale_dailyprice,
                customer=customer,
                companyseller =companyseller,
                sale_date=sale_date,
                sale_price=sale_price,  # ارسال قیمت به عنوان Decimal
                net_sale_price=net_sale_price,
                discount=discount,
                notes=notes,
                invoice_serial=invoice_serial,
            )
            invoice.save()

            cart = request.session.get('sale_cart', [])

            if not cart:
                messages.error(request, 'سبد خرید خالی است.')
                return render(request, 'vitrin/create_sale_invoice.html', {'form': form})
            for item in cart:
                if item['type'] == 'craft':
                    piece = CraftPiece.objects.get(id=item['id'])
                    piece.sale_invoice = invoice
                else:
                    piece = OldPiece.objects.get(id=item['id'])
                    piece.sale_invoice = invoice
                piece.save()

            request.session['sale_cart'] = []
            return redirect('vitrin:sale_invoice_list')
        else:
            messages.error(request, 'اطلاعات شما کامل نیست. لطفاً فیلدهای فرم را بررسی کنید.')
            return render(request, 'vitrin/create_sale_invoice.html', {'form': form})
    else:
        form = SaleInvoiceForm()
    return render(request, 'vitrin/create_sale_invoice.html', {'form': form})


# ----------------------------------------------------
@login_required
def sale_invoice_detail(request, invoice_id):
    invoice = get_object_or_404(SaleInvoice, pk=invoice_id)
    payments = invoice.salepayments.all()
    craftpiece = invoice.crafted_golds.all()
    oldpiece = invoice.old_gold.all()

    # محاسبه مجموع وزن و قیمت
    total_net_weight = sum(item.net_weight or 0 for item in craftpiece) + sum(item.net_weight or 0 for item in oldpiece)
    total_sale_price = sum(item.sale_price or 0 for item in craftpiece) + sum(item.sale_price or 0 for item in oldpiece)

    context = {
        'invoice': invoice,
        'craftpiece': craftpiece,
        'oldpiece': oldpiece,
        'payments': payments,
        'total_net_weight': total_net_weight,
        'total_sale_price': total_sale_price,

    }
    return render(request, 'vitrin/sale_invoice_detail.html', context)


# ----------------------لیست فاکتور فروش-------------

@login_required
def sale_invoice_list(request):
    if request.GET:
        request.session['sale_invoice_list_filters'] = {
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
            'companyseller': request.GET.get('companyseller', ''),
            'customer': request.GET.get('customer', ''),
        }

    filters = request.session.get('sale_invoice_list_filters', {})
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')
    companyseller = filters.get('companyseller', '')
    customer_name = filters.get('customer', '')
    invoices = SaleInvoice.objects.all()
    start_date_jalali = ''
    end_date_jalali = ''

    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()
        invoices = invoices.filter(sale_date__range=(start_date_gregorian, end_date_gregorian))

        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y/%m/%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y/%m/%d')

    if companyseller:
        invoices = invoices.filter(companyseller__name__icontains=companyseller)

    if customer_name:
        invoices = invoices.filter(
            Q(customer__last_name__icontains=customer_name) |
            Q(customer__first_name__icontains=customer_name)
        )
    invoices = invoices.order_by('-sale_date')
    if not (start_date or end_date or companyseller or customer_name):
        invoices = invoices[:10]

    invoice_data = []
    all_sale_price = 0
    all_discount = 0
    all_net_weight = 0
    weighted_gold_price_sum = 0  # متغیر برای جمع کل (قیمت روز × وزن)
    total_sale_price_difference = 0
    sale_price_difference = 0

    for invoice in invoices:
        total_sale_price = invoice.sale_price or 0
        total_discount = invoice.discount or 0
        total_net_weight = (
                                   invoice.crafted_golds.aggregate(total_weight=Sum('net_weight'))['total_weight'] or 0
                           ) + (
                                   invoice.old_gold.aggregate(total_weight=Sum('net_weight'))['total_weight'] or 0
                           )

        # محاسبه مجموع قیمت فروش واقعی آیتم‌ها
        crafted_total_sale_price = invoice.crafted_golds.aggregate(total=Sum('sale_price'))['total'] or 0
        old_total_sale_price = invoice.old_gold.aggregate(total=Sum('sale_price'))['total'] or 0
        calculated_total_sale_price = crafted_total_sale_price + old_total_sale_price

        sale_price_difference =  total_sale_price - calculated_total_sale_price
        total_sale_price_difference += sale_price_difference

        gold_price = invoice.sale_dailyprice or 0  # قیمت روز طلا برای فاکتور
        weighted_gold_price_sum += gold_price * total_net_weight

        invoice.total_sale_price = total_sale_price
        invoice.total_discount = total_discount
        invoice.total_net_weight = total_net_weight

        # اختلاف مبلغ کل فاکتور با مبلغ پرداخت‌شده
        unpaid_amount = (invoice.net_sale_price or 0) - (invoice.total_paid or 0)

        invoice_data.append({
            'invoice': invoice,
            'calculated_total_sale_price': calculated_total_sale_price,
            'sale_price_difference': sale_price_difference,
            'unpaid_amount': unpaid_amount,
        })
        all_sale_price += total_sale_price
        all_discount += total_discount
        all_net_weight += total_net_weight

        # محاسبه میانگین وزنی قیمت طلا
    weighted_avg_gold_price = (
       int(weighted_gold_price_sum / all_net_weight) if all_net_weight > 0 else 0
    )
    context = {
        'invoices': invoices,
        'customer_name': customer_name,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'companyseller': companyseller,
        'filters': filters,
        'invoice_data': invoice_data,
        'all_sale_price': all_sale_price,
        'all_discount': all_discount,
        'all_net_weight': all_net_weight,
        'weighted_avg_gold_price': weighted_avg_gold_price,
        'sale_price_difference':sale_price_difference,
        'total_sale_price_difference': total_sale_price_difference,

    }
    return render(request, 'vitrin/sale_invoice_list.html', context)
# ------------------------لیست فروش کالای زینتی و مستعمل-------------------------



@login_required
def sale_piece_list(request):
    filters_applied = False
    if request.GET:
        if request.GET.get('clear_filters'):
            request.session.pop('vitrin_filters', None)
            return redirect('vitrin:sale_piece_list')
        else:
            request.session['vitrin_filters'] = {
                'start_date': request.GET.get('start_date', ''),
                'end_date': request.GET.get('end_date', ''),
                'companyseller': request.GET.get('companyseller', ''),
                'customer': request.GET.get('customer', ''),
                'gold_type': request.GET.getlist('gold_type', [])
            }

    filters = request.session.get('vitrin_filters', {})
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')
    companyseller = filters.get('companyseller', '')
    customer_name = filters.get('customer', '')
    gold_type = filters.get('gold_type', [])

    if any([start_date, end_date, companyseller, customer_name, gold_type]):
        filters_applied = True

    craftpieces = CraftPiece.objects.filter(is_sold=True).select_related('sale_invoice__customer', 'supplier')
    oldpieces = OldPiece.objects.filter(is_sold=True).select_related('sale_invoice__customer', 'supplier')

    start_date_jalali = ''
    end_date_jalali = ''

    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()

        craftpieces = craftpieces.filter(sale_invoice__sale_date__range=(start_date_gregorian, end_date_gregorian))
        oldpieces = oldpieces.filter(sale_invoice__sale_date__range=(start_date_gregorian, end_date_gregorian))

        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y/%m/%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y/%m/%d')

    if companyseller:
        craftpieces = craftpieces.filter(sale_invoice__companyseller__name__icontains=companyseller)
        oldpieces = oldpieces.filter(sale_invoice__companyseller__name__icontains=companyseller)

    if customer_name:
        customer_name = customer_name.strip()
        craftpieces = craftpieces.filter(
            Q(sale_invoice__customer__last_name__icontains=customer_name) |
            Q(sale_invoice__customer__first_name__icontains=customer_name) |
            Q(
                (Q(sale_invoice__customer__first_name__isnull=False) & Q(
                    sale_invoice__customer__last_name__isnull=False)) &
                Q(
                    sale_invoice__customer__first_name__icontains=customer_name.split()[0]
                ) & Q(
                    sale_invoice__customer__last_name__icontains=customer_name.split()[-1])))

        oldpieces = oldpieces.filter(
            Q(sale_invoice__customer__last_name__icontains=customer_name) |
            Q(sale_invoice__customer__first_name__icontains=customer_name) |
            Q(
                (Q(sale_invoice__customer__first_name__isnull=False) & Q(
                    sale_invoice__customer__last_name__isnull=False)) &
                Q(
                    sale_invoice__customer__first_name__icontains=customer_name.split()[0]
                ) & Q(
                    sale_invoice__customer__last_name__icontains=customer_name.split()[-1]) ) )

    if gold_type:
        if 'craft' in gold_type and 'old' not in gold_type:
            oldpieces = OldPiece.objects.none()
        elif 'old' in gold_type and 'craft' not in gold_type:
            craftpieces = CraftPiece.objects.none()

    combined_pieces = list(craftpieces) + list(oldpieces)

    def get_sale_date(piece):
        return piece.sale_invoice.sale_date if piece.sale_invoice and piece.sale_invoice.sale_date else piece.created_at

    combined_pieces.sort(key=get_sale_date, reverse=True)

    if not filters_applied:
        combined_pieces = combined_pieces[:10]

    pieces = []
    total_net_weight = Decimal('0.00')
    total_sale_price = 0
    weighted_dailyprice_sum = Decimal('0.00')
    total_profit_value = Decimal('0.00')

    for piece in combined_pieces:
        piece_type = 'craft' if isinstance(piece, CraftPiece) else 'old'

        sale_ojrat = piece.sale_ojrat or Decimal('0.00')
        seller_profit_percent = piece.seller_profit_percent or Decimal('0.00')
        net_weight = piece.net_weight if piece.net_weight is not None else Decimal('0.00')
        sale_price_ojrat = piece.sale_price_ojrat or 0
        if isinstance(piece, OldPiece):
            buy_price_ojrat = 0
        else:
            buy_price_ojrat = piece.buy_price_ojrat or 0
        # محاسبه سود ریالی اجرت
        rial_profit = sale_price_ojrat - buy_price_ojrat
        sale_dailyprice = Decimal('0.00')
        if hasattr(piece, 'sale_invoice') and piece.sale_invoice:
            sale_dailyprice_value = getattr(piece.sale_invoice, 'sale_dailyprice', 0) or 0
            sale_dailyprice = Decimal(str(sale_dailyprice_value))

        if isinstance(piece, CraftPiece):
            buy_ojrat = piece.buy_ojrat or Decimal('0.00')
        else:
            buy_ojrat = Decimal('0.00')
        profit_per_gram = sale_ojrat - buy_ojrat + seller_profit_percent


        # جلوگیری از تقسیم بر صفر
        if sale_dailyprice != 0:
            profit_value = ((profit_per_gram * net_weight) / 100) + (
                        (sale_price_ojrat - buy_price_ojrat) / sale_dailyprice)
        else:
            profit_value = ((profit_per_gram * net_weight) / 100)


        total_profit_value += profit_value
        if net_weight > 0:
            percent_profit = (profit_value * 100) / net_weight
        else:
            percent_profit = Decimal('0.00')
        pieces.append({
            'piece': piece,
            'type': piece_type,
            # سود وزنی
            'profit_value': profit_value.quantize(Decimal('0.01')),
            # درصد سود
            'percent_profit': percent_profit.quantize(Decimal('0.01')),
            'rial_profit': rial_profit,
        })

        if net_weight and piece.sale_price:
            total_net_weight += net_weight
            total_sale_price += piece.sale_price
            if piece.sale_invoice and piece.sale_invoice.sale_dailyprice:
                weighted_dailyprice_sum += net_weight * Decimal(piece.sale_invoice.sale_dailyprice)

    weighted_avg_dailyprice = int(
        (weighted_dailyprice_sum / total_net_weight).quantize(Decimal('0.01'))
        if total_net_weight > 0 else 0)

        #  دردص سود کلی
    if total_net_weight != 0:
        total_profit_percentage = (100 * total_profit_value / total_net_weight)
    else:
        total_profit_percentage = 0

    total_piece_count = len(combined_pieces)

    context = {
        'companyseller': companyseller,
        'customer_name': customer_name,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'filters': filters,
        'gold_type': gold_type,
        'pieces': pieces,
        'total_net_weight': total_net_weight,
        'total_sale_price': total_sale_price,
        'weighted_avg_dailyprice': weighted_avg_dailyprice,
        'total_profit_value': total_profit_value.quantize(Decimal('0.01')),
        'total_profit_percentage':total_profit_percentage,
        'total_piece_count': total_piece_count,

    }

    return render(request, 'vitrin/sale_piece_list.html', context)

# ----------------------------------------------------------