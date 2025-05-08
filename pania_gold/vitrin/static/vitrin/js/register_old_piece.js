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
    var netWeight = document.getElementById('id_net_weight').value;

    if (netWeight) {
        var weight = parseFloat(netWeight);
        if (isNaN(weight)) {
            console.error("Net weight is not a valid number.");
            return;
        }

        // گرفتن بخش صحیح و اعشاری
        var intPart = Math.floor(weight);  // بخش صحیح
        var decPart = Math.round((weight - intPart) * 100);  // بخش اعشاری

        // اطمینان از اینکه بخش اعشاری دو رقمه است
        if (decPart < 10) {
            decPart = '0' + decPart;
        }

        // فرمت وزن به صورت 4 رقم (مثلاً 0150)
        var formattedWeight = intPart.toString().padStart(2, '0') + decPart;

        // گرفتن سه رقم انتهایی timestamp
        var timestamp = Math.floor(Date.now() / 1000);  // برحسب ثانیه
        var lastThreeDigits = timestamp.toString().slice(-2);

        // تولید کد نهایی
        var generatedCode = 'OL' + lastThreeDigits + '-' + formattedWeight;

        // مقداردهی به فیلد کد
        document.getElementById('id_code').value = generatedCode;
    } else {
        console.warn("Net weight must be filled to generate the code.");
    }
}

// اجرای تابع هنگام تغییر مقدار وزن
document.getElementById('id_net_weight').addEventListener('input', generateCode);
