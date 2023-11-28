document.addEventListener('DOMContentLoaded', function () {
    const quantityButtons = document.querySelectorAll('.quantity-btn');

    quantityButtons.forEach(function (button) {
        if (button.innerText === '-') {
            button.action = 'decrement';
        } else if (button.innerText === '+') {
            button.action = 'increment';
        }

        button.addEventListener('click', function (event) {
            const itemId = button.getAttribute('data-item-id');
            const itemQuantityElement = document.querySelector(`.item-quantity[data-item-id="${itemId}"]`);
            let itemQuantity = parseInt(itemQuantityElement.textContent);

            if (button.action === 'decrement') {
                if (itemQuantity > 1) {
                    itemQuantity -= 1;
                }
            } else if (button.action === 'increment') {
                itemQuantity += 1;
            }

            itemQuantityElement.textContent = itemQuantity;
        });
    });

    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCartButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            const itemId = button.getAttribute('data-item-id');

            // Find the item quantity for this item
            const itemQuantityElement = document.querySelector(`.item-quantity[data-item-id="${itemId}"]`);
            const quantity = itemQuantityElement.textContent;

            addToCart(itemId, quantity);
        });
    });
});

function addToCart(itemId, quantity) {
    fetch(`/add_to_cart/${itemId}/${quantity}/`)
        .then(response => response.json())
        .then(data => {
            // Handle the response if needed (e.g., update cart icon)
        });
}


document.addEventListener('DOMContentLoaded', function () {
    // Make an AJAX request to get the item count
    fetch('/api/cart_item_count/')
        .then(response => response.json())
        .then(data => {
            const itemCount = data.item_count;

            // Display the item count only if it's greater than 0
            if (itemCount > 0) {
                const itemCountElement = document.getElementById('cart-item-count');
                itemCountElement.textContent = itemCount;
            }
        })
        .catch(error => {
            console.error('Error fetching item count:', error);
        });
});

document.addEventListener('DOMContentLoaded', function() {
    const categoryButton = document.getElementById('category-button');
    const categoryContent = document.getElementById('category-content');

    // Flag to track the dropdown state
    let isDropdownOpen = false;

    categoryButton.addEventListener('click', function() {
        isDropdownOpen = !isDropdownOpen;
        categoryContent.style.display = isDropdownOpen ? 'block' : 'none';
    });

    // Close the dropdown when clicking outside the category button and items
    document.addEventListener('click', function(event) {
        if (isDropdownOpen && event.target !== categoryButton && !categoryContent.contains(event.target)) {
            isDropdownOpen = false;
            categoryContent.style.display = 'none';
        }
    });
});
// Add a click event listener to the heart icon
const wishlistIcons = document.querySelectorAll('.wishlist-icon');

wishlistIcons.forEach((icon) => {
    icon.addEventListener('click', function (event) {
        const itemId = icon.getAttribute('data-item-id');

        // Send an AJAX request to add or remove the item from the wishlist
        fetch(`/add_to_wishlist/${itemId}/`)
            .then((response) => response.json())
            .then((data) => {
                // Toggle the "added" class to change the icon color
                if (icon.classList.contains('added')) {
                    icon.classList.remove('added');
                } else {
                    icon.classList.add('added');
                }
            })
            .catch((error) => {
                console.error('Error adding to wishlist:', error);
            });
    });
});
function updateWishlistCount() {
    fetch('/api/wishlist_item_count/')
        .then(response => response.json())
        .then(data => {
            const wishlistCount = data.item_count;
            const wishlistCountElement = document.getElementById('wishlist-count');

            if (wishlistCount > 0) {
                wishlistCountElement.textContent = wishlistCount;
                wishlistCountElement.style.display = 'block';
            } else {
                wishlistCountElement.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching wishlist count:', error);
        });
}

// Call the function to update the wishlist count
updateWishlistCount();




