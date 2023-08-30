document.querySelectorAll('.add-button').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();

        let itemId = button.getAttribute('data-id');
        let form = document.querySelector('#form-' + itemId);
        let quantityInput = form.querySelector('.quantity-input');
        let quantity = parseInt(quantityInput.value, 10);
        console.log(quantity);
        if (quantity < 1){
            showPopup("Quantity can not be less than 1");
        } else {
            let cartData = JSON.parse(localStorage.getItem('cart')) || {};
            cartData[itemId] = quantity;
            localStorage.setItem('cart', JSON.stringify(cartData));
            showPopup("item added successfully");
        }

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