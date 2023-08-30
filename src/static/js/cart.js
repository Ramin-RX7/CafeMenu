document.querySelectorAll('.add-button').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();

        let itemId = button.getAttribute('data-id');
        let form = document.querySelector('#form-' + itemId);
        let quantityInput = form.querySelector('.quantity-input');
        let quantity = parseInt(quantityInput.value, 10);

        let cartData = JSON.parse(localStorage.getItem('cart')) || {};

        cartData[itemId] = quantity;

        localStorage.setItem('cart', JSON.stringify(cartData));

        let quantityElement = document.getElementById(`item-quantity-${itemId}`)
        quantityElement.textContent = quantity;

        showPopup("Item quantity changed")
    });
});

document.querySelectorAll('.del-button').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        console.log("here");

        let itemId = button.getAttribute('value');

        let cartData = JSON.parse(localStorage.getItem('cart')) || {};

        delete cartData[itemId];

        let new_data = JSON.stringify(cartData)
        localStorage.setItem('cart', new_data);

        let foodSection = document.getElementById(`food-${itemId}`)
        foodSection.remove()

        showPopup("Item deleted")
    });
});


function showPopup(text){
    let popup = document.getElementById('popup');
    popup.style.display = 'block';
    popup.textContent = text

    setTimeout(function() {
        popup.style.display = 'none';
    }, 2500);
}


document.getElementById('sendDataButton').addEventListener('click', function() {
    function setCookie(name, value, days) {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
    }
    let cart = JSON.parse(localStorage.getItem('cart'));
    let cartDataString = JSON.stringify(cart);
    setCookie('cart', cartDataString, 0.01);
    localStorage.removeItem('cart');
    orderForm.submit();
});

