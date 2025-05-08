from django.shortcuts import render,get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch
import jdatetime
from decimal import Decimal
import time
from django.core.paginator import Paginator
from .models import MeltPiece,SaleMeltInvoice
from vitrin.forms import OldPieceForm,UploadImageForm,SaleInvoiceForm
from .forms import SaleMeltInvoiceForm
from django.contrib import messages
from django.http import JsonResponse




# --------------------------------

@login_required
def meltupload_image(request, golditem_id):
    form = UploadImageForm()
    gold_item = None
    models = [ MeltPiece]
    for model in models:
        try:
            gold_item = model.objects.get(id=golditem_id)
            break
        except model.DoesNotExist:
            continue
    if not gold_item:
        return render(request, 'meltvitrin/meltcart_detail_not_found.html')
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            gold_item.image = form.cleaned_data['image']
            gold_item.save()
            messages.success(request, "تصویر با موفقیت آپلود شد")
            return redirect('meltvitrin:meltcart_detail', golditem_id=golditem_id)
        else:
            messages.error(request, "خطا در آپلود تصویر. لطفاً مجدداً تلاش کنید.")
    return render(request, 'meltvitrin/meltcart_detail.html', {'vitrin': gold_item, 'form': form})
# ---------------------------------
@login_required
def meltcart_detail(request, gold_type, golditem_id):
    vitrin = None
    form = UploadImageForm()

    if gold_type == "melt":
        try:
            vitrin = MeltPiece.objects.get(id=golditem_id)
        except MeltPiece.DoesNotExist:
            return render(request, 'meltvitrin/meltcart_detail_not_found.html')

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            vitrin.image = form.cleaned_data['image']
            vitrin.save()
            messages.success(request, "تصویر با موفقیت آپلود شد.")
            return redirect('meltvitrin:meltcart_detail', gold_type=gold_type, golditem_id=golditem_id)
        else:
            messages.error(request, "خطا در آپلود تصویر. لطفاً مجدداً تلاش کنید.")

    return render(request, 'meltvitrin/meltcart_detail.html', {'vitrin': vitrin, 'form': form})

# ---------------------------------------
@login_required
def meltvitrin_list(request):
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

    meltpieces = MeltPiece.objects.filter(is_sold=False).select_related('sale_invoice__customer', 'supplier')
    query_filter = Q()
    if name:
        query_filter |= Q(name__icontains=name) | Q(code__icontains=name)
    if code:
        query_filter |= Q(code__icontains=code)
    meltpieces = meltpieces.filter(query_filter)
    # فیلتر بر اساس نوع طلا
    selected_pieces = []
    if 'melt' in gold_type:
        selected_pieces.extend(meltpieces)
    # اگر هیچ فیلتر نوع انتخاب نشده باشد، همه موارد نمایش داده شوند
    if not gold_type:
        selected_pieces =  list(meltpieces)

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
            'melt'
        )}
        for piece in page_obj
    ]
    # دریافت تعداد کالاهای موجود در سبد خرید
    meltcart = request.session.get('sale_cart_melt', [])
    cart_count = len(meltcart)  # شمارش تعداد کالاها در سبد خرید
    # محاسبه مجموع وزن و تعداد قطعات
    total_weight = sum([piece.net_weight or 0 for piece in selected_pieces])
    total_count = len(selected_pieces)
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
    }
    return render(request, 'meltvitrin/meltvitrin_list.html', context)
# -----------------------------------------
@login_required
def add_to_invoice_melt(request, piece_type, piece_id):
    meltcart = request.session.get('sale_cart_melt', [])
    if piece_type == 'melt':
        piece = MeltPiece.objects.get(id=piece_id)  # فقط کالاهای فروخته نشده
    else:
        return redirect('meltvitrin:meltvitrin_list')
    meltcart.append({
        'type': piece_type,
        'id': piece_id,
        'name': piece.name,
        'net_weight': float(piece.net_weight),
        'code': piece.code,
        'sale_ojrat': float(piece.sale_ojrat),
        'image': piece.image.url if piece.image else None,
    })

    request.session['sale_cart_melt'] = meltcart
    piece.is_sold = True
    piece.save()
    cart_count = len(meltcart)
    return JsonResponse({'success': True, 'cart_count': cart_count})

# ------------------------------------------------
@login_required
def remove_from_invoice_melt(request):
    if request.method == 'POST':
        piece_id = request.POST.get('piece_id')
        piece_type = request.POST.get('piece_type')
        if not piece_id or not piece_type:
            messages.error(request, 'اطلاعات مورد نیاز کامل نیست.')
            return redirect('meltvitrin:create_sale_melt_invoice')
        try:
            piece_id = int(piece_id)
        except (ValueError, TypeError):
            messages.error(request, 'آیدی کالا معتبر نیست.')
            return redirect('meltvitrin:create_sale_melt_invoice')

        meltcart = request.session.get('sale_cart_melt', [])
        meltcart = [item for item in meltcart if not (item['id'] == piece_id and item['type'] == piece_type)]
        request.session['sale_cart_melt'] = meltcart
        if piece_type == 'melt':
            try:
                piece = MeltPiece.objects.get(id=piece_id)
            except MeltPiece.DoesNotExist:
                messages.error(request, 'کالای مورد نظر یافت نشد.')
                return redirect('meltvitrin:create_sale_melt_invoice')

        piece.is_sold = False
        piece.save()
        messages.success(request, 'کالا از سبد حذف شد.')
        return redirect('meltvitrin:create_sale_melt_invoice')
    else:
        return redirect('meltvitrin:create_sale_melt_invoice')





# --------------------------------------------
@login_required
def create_sale_melt_invoice(request):
    if request.method == 'POST':
        form = SaleMeltInvoiceForm(request.POST)
        jalali_date = request.POST.get('sale_date')
        if jalali_date:
            try:
                formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
                form.data = form.data.copy()  # کپی کردن داده‌های فرم
                form.data['sale_date'] = formatted_date  # تغییر تاریخ در داده‌ها
            except ValueError:
                messages.error(request, 'تاریخ وارد شده نامعتبر است.')
                return render(request, 'meltvitrin/create_sale_melt_invoice.html', {'form': form})

        sale_dailyprice = request.POST.get('sale_dailyprice')
        if sale_dailyprice:
            form.data = form.data.copy()  # کپی کردن داده‌های فرم
            form.data['sale_dailyprice'] = sale_dailyprice  # تغییر قیمت روزانه در داده‌ها

        if form.is_valid():
            sale_dailyprice = form.cleaned_data.get('sale_dailyprice')
            customer = form.cleaned_data.get('customer')
            companyseller = form.cleaned_data.get('companyseller')
            sale_date = form.cleaned_data.get('sale_date')
            total_sale_price = form.cleaned_data.get('total_sale_price')
            discount = form.cleaned_data.get('discount')
            notes = form.cleaned_data.get('notes')
            # ایجاد فاکتور
            invoice = SaleMeltInvoice(
                sale_dailyprice=sale_dailyprice,
                customer=customer,
                companyseller=companyseller,
                sale_date=sale_date,
                total_sale_price=total_sale_price,
                discount=discount,
                notes=notes
            )
            invoice.save()

            meltcart = request.session.get('sale_cart_melt', [])
            if not meltcart:
                messages.error(request, 'سبد خرید خالی است.')
                return render(request, 'meltvitrin/create_sale_melt_invoice.html', {'form': form})
            for item in meltcart:
                if item['type'] == 'melt':
                    try:
                        piece = MeltPiece.objects.get(id=item['id'])
                        piece.sale_invoice = invoice

                        # محاسبه قیمت فروش مشابه جاوااسکریپت
                        net_weight = float(piece.net_weight)
                        sale_ojrat = float(piece.sale_ojrat)
                        j8 = net_weight * (1 + (sale_ojrat / 100))
                        j10 = j8 * (1 + 0.0)
                        j14 = int(j10 * sale_dailyprice)
                        m6 = int(net_weight * sale_dailyprice)
                        m10 = int((sale_ojrat / 100) * m6)
                        m12 = int((m6 + m10) * 0.0)
                        sale_tax = int((m12 + m10) * 0.1)
                        sale_price = int(j14 + sale_tax)

                        piece.sale_price = sale_price
                        piece.save()
                    except MeltPiece.DoesNotExist:
                        messages.error(request, f'کالای با شناسه {item["id"]} یافت نشد.')
            request.session['sale_cart_melt'] = []
            return redirect('meltvitrin:sale_invoice_melt_list')
        else:
            messages.error(request, 'اطلاعات شما کامل نیست. لطفاً فیلدهای فرم را بررسی کنید.')
            return render(request, 'meltvitrin/create_sale_melt_invoice.html', {'form': form})
    else:
        form = SaleMeltInvoiceForm()
    return render(request, 'meltvitrin/create_sale_melt_invoice.html', {'form': form})
# ------------------------------------------------


# ------------------------------------------------
@login_required
def sale_invoice_melt_detail(request, invoice_id):
    invoice = get_object_or_404(SaleMeltInvoice, pk=invoice_id)
    meltpieces = invoice.melt_golds.all()

    context = {
        'invoice': invoice,
        'meltpieces': meltpieces,
    }
    return render(request, 'meltvitrin/sale_invoice_melt_detail.html', context)


# -----------------------------------------------------
@login_required
def sale_invoice_melt_list(request):
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
    invoices = SaleMeltInvoice.objects.all()
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

    for invoice in invoices:
        total_sale_price = invoice.total_sale_price or 0
        total_discount = invoice.discount or 0

        invoice.total_sale_price = total_sale_price
        invoice.total_discount = total_discount

        invoice_data.append({
            'invoice': invoice,
        })
        all_sale_price += total_sale_price
        all_discount += total_discount
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
    }
    return render(request, 'meltvitrin/sale_invoice_melt_list.html', context)

# ------------------------------------
@login_required
def sale_meltpiece_list(request):
    if request.GET:
        request.session['sale_meltpiece_list_filters'] = {
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
            'companyseller': request.GET.get('companyseller', ''),
            'customer': request.GET.get('customer', ''),
        }

    filters = request.session.get('sale_meltpiece_list_filters', {})
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')
    companyseller = filters.get('companyseller', '')
    customer_name = filters.get('customer', '')
    sale_piece = MeltPiece.objects.filter(is_sold=True)
    start_date_jalali = ''
    end_date_jalali = ''

    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))

        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()

        sale_piece = sale_piece.filter(sale_date__range=(start_date_gregorian, end_date_gregorian))

        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y/%m/%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y/%m/%d')

    if companyseller:
        sale_piece = sale_piece.filter(sale_invoice__companyseller__name__icontains=companyseller)

    if customer_name:
        sale_piece = sale_piece.filter(
            Q(sale_invoice__customer__last_name__icontains=customer_name) |
            Q(sale_invoice__customer__first_name__icontains=customer_name)
        )
    sale_piece = sale_piece.order_by('-sale_date')
    if not (start_date or end_date or companyseller or customer_name):
        sale_piece = sale_piece[:10]
    context = {
        'sale_piece': sale_piece,
        'customer_name': customer_name,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'companyseller': companyseller,
        'filters': filters,
    }
    return render(request, 'meltvitrin/sale_meltpiece_list.html', context)

# ---------------------------------------------