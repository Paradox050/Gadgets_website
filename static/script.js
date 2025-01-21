
//swap images on click
function swapImage(imageUrl) {
    // Update the main image
    document.getElementById('main-image').src = imageUrl;

    // Remove the 'selected' class from all color variants
    const variants = document.querySelectorAll('.variant-image');
    variants.forEach(variant => {
        variant.classList.remove('selected');
    });

    // Add the 'selected' class to the clicked variant
    const clickedVariant = Array.from(variants).find(variant => variant.getAttribute('src') === imageUrl);
    if (clickedVariant) {
        clickedVariant.classList.add('selected');
    }
}

//cart

document.addEventListener('DOMContentLoaded', function() {
    // Get all the increase and decrease buttons
    const decreaseButtons = document.querySelectorAll('.decrease-qty');
    const increaseButtons = document.querySelectorAll('.increase-qty');

    // Add event listener to each decrease button
    decreaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = button.getAttribute('data-id');  // Get item ID
            updateQuantity(itemId, -1);  // Decrease quantity by 1
        });
    });

    // Add event listener to each increase button
    increaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = button.getAttribute('data-id');  // Get item ID
            updateQuantity(itemId, 1);  // Increase quantity by 1
        });
    });
});

function updateQuantity(itemId, quantityChange) {
    const timestamp = new Date().getTime();  // Add a unique timestamp to the URL
    fetch(`/update_cart/${itemId}/${quantityChange}/?timestamp=${timestamp}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Log the response data for debugging
        const quantityElement = document.querySelector(`#item-${itemId} .quantity`);
        if (quantityElement) {
            quantityElement.textContent = data.new_quantity;
        }

        // Update the subtotal and total prices
        document.querySelector('#total-summary .total-details:nth-child(1) span').textContent = `₹${data.new_subtotal}`;
        document.querySelector('#total-summary .total-details:nth-child(2) span').textContent = `₹${data.new_total}`;
    })
    .catch(error => {
        console.error('Error updating cart:', error);
    });
}

