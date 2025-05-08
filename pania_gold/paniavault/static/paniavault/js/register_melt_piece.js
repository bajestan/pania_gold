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

// تابع برای محاسبه وزن عیار 750
function calculateNetWeight() {
    const karatField = document.getElementById('id_karat');
    const weightField = document.getElementById('id_weight');
    const netWeightField = document.getElementById('id_net_weight'); // فیلد وزن عیار 750

    // بررسی ورودی ها
    const karat = karatField ? parseFloat(karatField.value) : 0;
    const weight = weightField ? parseFloat(weightField.value) : 0;

    // اگر هر دو مقدار وزن و عیار صحیح بودند
    if (!isNaN(karat) && !isNaN(weight) && karat > 0 && weight > 0) {
        // محاسبه وزن عیار 750
        const netWeight = weight * (karat / 750);

        // نمایش وزن عیار 750 در فیلد مربوطه
        if (netWeightField) {
            netWeightField.value = netWeight.toFixed(2); // نمایش با دو رقم اعشار
            netWeightField.readOnly = true; // غیرقابل ویرایش کردن فیلد
        }
    }
}

// تابع برای تولید کد کالا
function generateCode() {
    const karatField = document.getElementById('id_karat');
    const weightField = document.getElementById('id_weight');
    const codeField = document.getElementById('id_code');

    const karat = karatField ? parseFloat(karatField.value) : null;
    const weight = weightField ? parseFloat(weightField.value) : null;

    if (karat && weight) {
        // بخش صحیح و اعشاری وزن
        const intPart = Math.floor(weight);
        const decPart = Math.round((weight - intPart) * 100).toString().padStart(2, '0');
        const formattedWeight = `${intPart.toString().padStart(2, '0')}${decPart}`;

        // کاراکترهای عیار
        const formattedKarat = Math.floor(karat).toString().padStart(3, '0');

        // تولید بخش یکتای تایم‌استمپ
        const timestamp = new Date().getTime().toString().slice(-1); // 1 کاراکتر آخر

        // تولید کد نهایی با فرمت جدید
        const generatedCode = `ME${timestamp}-${formattedKarat}-${formattedWeight}`;

        // تنظیم مقدار فیلد کد
        if (codeField) {
            codeField.value = generatedCode;
        }
    }
}

// اجرای تابع با تغییر فیلدها
document.getElementById('id_karat').addEventListener('input', function() {
    calculateNetWeight();
    generateCode();
});
document.getElementById('id_weight').addEventListener('input', function() {
    calculateNetWeight();
    generateCode();
});

// در صورتی که فرم با مقدار پیش‌فرض صفر لود شود، مقدار محاسبه‌شده در فیلد `net_weight` قرار می‌گیرد
window.addEventListener('load', function() {
    const netWeightField = document.getElementById('id_net_weight');
    if (netWeightField && netWeightField.value === '0') {
        calculateNetWeight(); // محاسبه مجدد در صورت لود فرم با مقدار پیش‌فرض
    }
});
