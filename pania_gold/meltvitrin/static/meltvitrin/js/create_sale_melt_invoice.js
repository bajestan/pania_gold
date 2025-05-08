$(document).ready(function () {
    jalaliDatepicker.startWatch({
        minDate: "attr",
        maxDate: "attr"
    });

    // حذف پیام‌ها بعد از 5 ثانیه
    setTimeout(function () {
        var messages = document.querySelector('.messages');
        if (messages) {
            messages.style.transition = "opacity 0.5s ease";
            messages.style.opacity = "0"; // محو شدن پیام
            setTimeout(function () {
                messages.remove(); // حذف پیام از DOM
            }, 500);
        }
    }, 5000);

    // فعال‌سازی select2
    $('.select2').select2({
        placeholder: "انتخاب مشتری",
        allowClear: true
    });

    // مقدار اولیه قیمت روزانه فروش
    var initialSaleDailyPrice = parseFloat($('input[name="sale_dailyprice"]').val());
    if (!isNaN(initialSaleDailyPrice) && initialSaleDailyPrice > 0) {
        updateSalePrices(initialSaleDailyPrice);
    }

    // تغییر قیمت روزانه و محاسبه قیمت نهایی فروش
    $('input[name="sale_dailyprice"]').on('input', function () {
        var saleDailyPrice = parseFloat($(this).val());
        if (!isNaN(saleDailyPrice) && saleDailyPrice > 0) {
            updateSalePrices(saleDailyPrice);
        } else {
            resetSalePrices();
        }
    });

    function updateSalePrices(saleDailyPrice) {
        var total = 0;
        $('#cart-table tbody tr').each(function () {
            var row = $(this);
            var netWeight = parseFloat(row.find('.net-weight').text());
            var saleOjrat = parseFloat(row.find('.sale-ojrat').text());
            if (isNaN(netWeight) || isNaN(saleOjrat)) return;

            var salePriceData = calculateSalePrice(netWeight, saleOjrat, saleDailyPrice);

            // مقداردهی فیلد مخفی و نمایش مقدار
            row.find('.sale-price-hidden').val(salePriceData.sale_price);
            row.find('.sale-price').text(salePriceData.sale_price.toLocaleString());

            total += salePriceData.sale_price;
        });
        updateTotalPrice(total);
    }



    function calculateSalePrice(netWeight, saleOjrat, saleDailyPrice) {
        var j8 = netWeight * (1 + (saleOjrat / 100));
        var j10 = j8 * (1 + 0.0);
        var j14 = Math.floor(j10 * saleDailyPrice);
        var m6 = Math.floor(netWeight * saleDailyPrice);
        var m10 = Math.floor((saleOjrat / 100) * m6);
        var m12 = Math.floor((m6 + m10) * 0.0);
        var saleTax = Math.floor((m12 + m10) * 0.1);
        var salePrice = Math.floor(j14 + saleTax);

        return {
            sale_price: salePrice,
            sale_tax: saleTax
        };
    }

    function updateTotalPrice(total) {
        $('#total-sale-price').text('قیمت کل فروش: ' + total.toLocaleString());
        $('input[name="sale_price"]').val(total);
    }

       // حذف کالا از فاکتور
    $('#cart-table').on('click', '.delete-item', function () {
        var row = $(this).closest('tr');
        row.remove(); // حذف ردیف از جدول
        updateTotalPriceAfterRemove(); // به روز رسانی مجموع قیمت‌ها بعد از حذف کالا
    });

   function resetSalePrices() {
    $('#cart-table tbody tr').each(function () {
        $(this).find('.sale-price').text('0'); // مقدار دیفالت صفر
        $(this).find('.sale-price-hidden').val(0); // مقدار دیفالت صفر در فیلد مخفی
    });
    updateTotalPrice(0);
    }

    function updateTotalPriceAfterRemove() {
        var total = 0;
        $('#cart-table tbody tr').each(function () {
            var salePrice = parseFloat($(this).find('.sale-price-hidden').val()) || 0; // مقدار خالی را 0 قرار می‌دهیم
            total += salePrice;
        });
        updateTotalPrice(total);
    }



    // بررسی تطابق تعداد قیمت‌ها و کالاها قبل از ارسال فرم
    $('form').on('submit', function (e) {
        var cartItems = $('#cart-table tbody tr').length;
        var salePrices = $('.sale-price-hidden').filter(function () {
            return $(this).val().trim() !== "";
        }).length;

        console.log('تعداد کالاها:', cartItems);
        console.log('تعداد قیمت‌های ثبت‌شده:', salePrices);

        if (cartItems !== salePrices) {
            e.preventDefault();
            alert('تعداد قیمت‌ها با تعداد کالاها مطابقت ندارد.');
        }
    });
});
