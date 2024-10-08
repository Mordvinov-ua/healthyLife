

// Когда html документ готов (прорисован)
$(document).ready(function () {
    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");

    // Ловим собыитие клика по кнопке добавить в корзину
     $(document).on("click", ".add-to-cart", function (e) {
         // Блокируем его базовое действие
         e.preventDefault();
         console.log("JavaScript начал свою работу");

         // Получаем id товара из атрибута data-product-id и data-variation-id
         var product_id = $(this).data("product-id");
         console.log("ID товара:", product_id);
         var variation_id = $(this).data("variation-id");
         console.log("ID вариации:", variation_id);
         // Из атрибута href берем ссылку на контроллер django
         var add_to_cart_url = $(this).attr("href");


         // делаем post запрос через ajax не перезагружая страницу
         $.ajax({
             type: "POST",
             url: add_to_cart_url,
             data: {
                product_id: product_id,
                variation_id: variation_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
             },
             success: function (data) {
                 // Сообщение
                 successMessage.html(data.message);
                 successMessage.fadeIn(200);
                 // Через 7сек убираем сообщение
                 setTimeout(function () {
                     successMessage.fadeOut(200);
                 }, 7000);

                 // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                 var cartItemsContainer = $("#cart-items-container");
                 cartItemsContainer.html(data.cart_items_html);

             },

             error: function (data) {
                 console.log("Ошибка при добавлении товара в корзину");
             },
         });
     });




    
    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();
         
         var cart_id = $(this).data("cart-id");
         var remove_from_cart = $(this).attr("href");
    
         
         $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                
                successMessage.html(data.message);
                successMessage.fadeIn(200);
                
                setTimeout(function () {
                    successMessage.fadeOut(200);
                }, 7000);

                
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

             },

             error: function (data) {
                 console.log("error");
             },
         });
     });




    // Теперь + - количества товара 
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Запускаем функцию определенную ниже
        // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
 
            success: function (data) {
                 // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(200);
                 // Через 7сек убираем сообщение
                setTimeout(function () {
                     successMessage.fadeOut(200);
                }, 7000);
 
                // Изменяем количество товаров в корзине
                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    }
});