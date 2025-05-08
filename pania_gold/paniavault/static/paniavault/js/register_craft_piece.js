

// جابجایی بین فیلدها با زدن کلید Enter
document.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // جلوگیری از ارسال فرم به صورت پیش‌فرض
        const formElements = Array.from(document.querySelectorAll("form input, form select, form textarea, form button"));
        const activeElement = document.activeElement;
        const currentIndex = formElements.indexOf(activeElement);
        const nextIndex = (currentIndex + 1) % formElements.length;

        if (nextIndex !== 0) {
            formElements[nextIndex].focus();
        }
    }
});




// تابع برای تولید کد کالا
function generateCode() {
    var goldType = document.getElementById('id_gold_type').value;
    var netWeight = document.getElementById('id_net_weight').value;
    var saleOjrat = document.getElementById('id_sale_ojrat').value;

    if (goldType && netWeight && saleOjrat) {
        // گرفتن دو حرف اول از نوع طلا
        var firstLetters = goldType.slice(0, 1).toUpperCase();

        // تبدیل وزن به عدد اعشاری
        var weight = parseFloat(netWeight);
        if (isNaN(weight)) {
            console.error("Net weight is not a valid number.");
            return;
        }

        // گرفتن بخش صحیح و اعشاری
        var intPart = Math.floor(weight);  // بخش صحیح
        var decPart = Math.round((weight - intPart) * 100);  // بخش اعشاری (دو رقم)

        // اگر بخش اعشاری فقط یک رقم بود، آن را به دو رقم تبدیل کنیم
        if (decPart < 10) {
            decPart = '0' + decPart;
        }

        // فرمت کردن وزن به صورت 4 کاراکتر
        var formattedWeight = intPart.toString().padStart(2, '0') + decPart;

        // فرمت کردن اجرت فروش به دو رقم
        var formattedSaleOjrat = saleOjrat.toString().padStart(2, '0');

        // استفاده از timestamp و کاهش طول آن به 2 رقم آخر
        var timestamp = new Date().getTime();
        var uniquePart = timestamp % 100;  // نمایش دو رقم آخر

        // تولید کد کالا
        var generatedCode = firstLetters + uniquePart + '-' + formattedWeight + '-' + formattedSaleOjrat;

        // مقداردهی به فیلد کد
        document.getElementById('id_code').value = generatedCode;
    } else {
        console.warn("All fields must be filled to generate the code.");
    }
}

// هر بار که فیلدها تغییر می‌کنند، تابع generateCode اجرا می‌شود
document.getElementById('id_gold_type').addEventListener('input', generateCode);
document.getElementById('id_net_weight').addEventListener('input', generateCode);
document.getElementById('id_sale_ojrat').addEventListener('input', generateCode);
