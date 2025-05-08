document.addEventListener("DOMContentLoaded", function () {
    const addToCartButtons = document.querySelectorAll(".add-to-invoice");
    const cartCountElement = document.getElementById("cart-count");

    addToCartButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            fetch(this.href, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    cartCountElement.textContent = data.cart_count;

                    // حذف محصول از لیست نمایش
                    const productCard = button.closest(".product-card");
                    if (productCard) {
                        productCard.remove();
                    }
                } else {
                    console.error("خطا در اضافه کردن به سبد خرید:", data.error);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
