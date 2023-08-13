function calculateCart(){
    const elementsToSum = document.querySelectorAll('.item-total-price');
    let sum = 0;
    elementsToSum.forEach(element => {
        sum += parseFloat(element.textContent);
    });
    const totalPrice = document.getElementById("total-price")
    if (totalPrice){
        totalPrice.textContent = sum.toString(10)+"$";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    calculateCart()
});