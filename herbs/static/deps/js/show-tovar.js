document.addEventListener('DOMContentLoaded', function() {
    //  Получаем элементы со страницы
    var variationSelect = document.getElementById('variation'); // Выбираем элемент <select> для вариаций
    var priceDisplay = document.getElementById('price'); // Выбираем элемент, в котором отображается цена
    var oldPriceDisplay = document.getElementById('old-price'); // Элемент для старой цены
    var ecoInfoDisplay = document.getElementById('econom_info'); // Элемент для polya ekonomii
    var butBuyContainer = document.querySelector('.but_buy'); // Контейнер для кнопки "Add to Cart"
    var oldPriceSpan = oldPriceDisplay.querySelector('span'); // Элемент span для старой цены
    var productIdInput = document.getElementById('product-id'); // Скрытое поле с ID товара
    var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]'); // CSRF-токен

    //  Получаем ID товара и CSRF-токен из скрытых полей
    var productId = productIdInput ? productIdInput.value : ''; // Если есть поле с ID товара, сохраняем его значение
    var csrfToken = csrfTokenInput ? csrfTokenInput.value : ''; // Если есть CSRF-токен, сохраняем его значение

    //  Функция для обновления цены и ID вариации
    function updatePriceAndVariationId() {
        if (variationSelect && priceDisplay && oldPriceDisplay && butBuyContainer) {
            var selectedOption = variationSelect.options[variationSelect.selectedIndex]; // Получаем выбранную опцию
            var newPrice = selectedOption.getAttribute('data-sellprice'); // Получаем цену из атрибута data-price выбранной опции
            var variationId = selectedOption.value; // Получаем ID вариации из значения выбранной опции
            var oldPrice = selectedOption.getAttribute('data-price'); // Получаем старую цену из атрибута data-price выбранной опции

            //  Обновляем цену на странице
            priceDisplay.textContent = newPrice+'$'; // Устанавливаем новое значение цены в элементе priceDisplay
            
            //  Обновляем старую цену
            if (newPrice !== oldPrice) {
                oldPriceSpan.textContent = oldPrice; // Устанавливаем старую цену
                oldPriceDisplay.style.display = 'flex'; // Показываем элемент с старой ценой
                priceDisplay.style.color = 'red'; // Устанавливаем цвет текста
                ecoInfoDisplay.style.display = 'flex'; // Показываем элемент с информацией о сэкономленной сумме
                ecoInfoDisplay.textContent = 'Saving: ' + (parseFloat(oldPrice.replace(',', '.')) - parseFloat(newPrice.replace(',', '.'))).toFixed(2) + '$' // Устанавливаем информацию о сэкономленной сумме
            } else {
                oldPriceDisplay.style.display = 'none'; // Скрываем элемент с старой ценой
                priceDisplay.style.color = 'black'; // Устанавливаем цвет текста
                ecoInfoDisplay.style.display = 'none';
            }
            //  Удаляем старую кнопку, если она есть
            var oldButton = document.querySelector('.button_buy_korb'); // Находим старую кнопку "Add to Cart"
            if (oldButton) {
                oldButton.remove(); // Удаляем старую кнопку
            }

            //  Создаем новую кнопку "Add to Cart"
            var newLink = document.createElement('a'); // Создаем новый элемент <a> для кнопки
            newLink.className = 'button_buy_korb add-to-cart'; // Устанавливаем класс кнопки
            newLink.href = '{% url "cart_add" %}'; // Устанавливаем ссылку на добавление в корзину
            newLink.setAttribute('data-product-id', productId); // Устанавливаем ID товара в атрибуте data-product-id
            newLink.setAttribute('data-variation-id', variationId); // Устанавливаем ID вариации в атрибуте data-variation-id

            var img = document.createElement('img'); // Создаем новый элемент <img> для кнопки
            img.className = 'add_in_korb'; // Устанавливаем класс изображения
            img.src = "{% static 'images/korb_add.png' %}"; // Устанавливаем путь к изображению

            newLink.appendChild(img); // Добавляем изображение в ссылку
            butBuyContainer.appendChild(newLink); // Добавляем кнопку в контейнер

            var textNode = document.createElement('span'); // Создаем элемент <span> для текста
            textNode.className = 'add-in-corb-text'; // Добавляем класс для текста
            textNode.textContent = 'Add in corb'; // Устанавливаем текст

            newLink.appendChild(textNode); // Добавляем текст в ссылку
            butBuyContainer.appendChild(newLink); // Добавляем кнопку в контейнер

            //  Обработчик клика по ссылке
            newLink.addEventListener('click', function(event) {
                event.preventDefault(); // Отменяем стандартное поведение ссылки

                fetch(newLink.href, {
                    method: 'POST', // Отправляем запрос методом POST
                    headers: {
                        'Content-Type': 'application/json', // Устанавливаем тип контента как JSON
                        'X-CSRFToken': csrfToken // Добавляем CSRF-токен в заголовок
                    },
                    body: JSON.stringify({
                        product_id: productId, // Передаем ID товара
                        variation_id: variationId // Передаем ID вариации
                    })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Ошибка сети'); // Если ошибка сети, выбрасываем исключение
                    }
                    return response.json(); // Возвращаем ответ в формате JSON
                })
                .then(data => {
                    console.log('Товар добавлен в корзину:', data); // Логируем данные ответа
                })
                .catch(error => {
                    console.error('Ошибка:', error); // Логируем ошибки
                });
            });

            //  Логируем изменения
            console.log('Обновленный Data Variation ID:', variationId); // Логируем обновленный ID вариации
            console.log('Обновленный Data Product ID:', productId); // Логируем обновленный ID товара
        }
    }

    //  Обработчик изменения выбора
    if (variationSelect) {
        variationSelect.addEventListener('change', updatePriceAndVariationId); // При изменении выбора вызываем функцию обновления
    }

    // Вызов функции сразу после загрузки страницы
    if (variationSelect) {
        updatePriceAndVariationId(); // Вызываем функцию для начального отображения цен и кнопки
    }

    // Слайдер
    var slides = document.querySelectorAll('.slide');
    var indicatorsContainer = document.getElementById('indicators');
    var currentIndex = 0;
    var totalSlides = slides.length;

    // Создание индикаторов
    for (var i = 0; i < totalSlides; i++) {
        var indicator = document.createElement('span');
        indicator.className = 'indicator';
        indicatorsContainer.appendChild(indicator);
    }

    function showSlide(index) {
        slides.forEach((slide, i) => {
            if (i === index) {
                slide.classList.add('active'); // Добавить класс active для отображения
            } else {
                slide.classList.remove('active'); // Убрать класс active для скрытия
            }
        });

        var indicators = document.querySelectorAll('.indicator');
        indicators.forEach((indicator, i) => {
            indicator.classList.toggle('active', i === index);
        });
    }

    document.querySelector('.next').addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % totalSlides;
        showSlide(currentIndex);
    });

    document.querySelector('.prev').addEventListener('click', function() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        showSlide(currentIndex);
    });

    // Показать первый слайд по умолчанию
    showSlide(currentIndex);
});