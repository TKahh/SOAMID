document.addEventListener("DOMContentLoaded", function (){
    let addToCartButtons = document.querySelectorAll('.add-to-cart');
    let cartButton = document.getElementById('cart-button');

    addToCartButtons.forEach(function (button){
        button.addEventListener('click', function (){
            let itemName = button.getAttribute('data-item');
            addToCart(itemName);
        })
    })

    function addToCart(itemName) {
        console.log(`Adding ${itemName} to cart`);
        fetch('/update_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item: itemName,
            }),
        })
            .then(response =>response.json())
            .then(data => {
                // Update the cart count on the existing Cart button
                let cartIcon = document.createElement('span');
                cartIcon.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cart" viewBox="0 0 16 16">
                        <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 12H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5M3.102 4l1.313 7h8.17l1.313-7zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4m7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4m-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2m7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
                    </svg>
                `;
                cartButton.innerHTML = '';
                cartButton.appendChild(cartIcon);

                if (data.cart_count > 0) {
                    let cartCountSpan = document.createElement('span');
                    cartCountSpan.innerText = data.cart_count;
                    cartButton.appendChild(cartCountSpan);

                    session = data.session;
                }
            })
            .catch(error => {
                console.error('Error: ', error);
            });
        console.log('Fetch request sent');
    }
});