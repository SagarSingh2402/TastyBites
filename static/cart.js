function loadCart(){

fetch("http://127.0.0.1:8000/cart/")
.then(response => response.json())
.then(data => {

    const container = document.getElementById("cart-container");
    const grandTotal = document.getElementById("grand-total");

    container.innerHTML = "";

    let total = 0;

    data.forEach(item => {

        total += item.price * item.quantity;

        container.innerHTML += `

        <div class="cart-card">

            <img src="${item.image}" alt="${item.item_name}">

            <div class="cart-info">

                <h2>${item.item_name}</h2>

                <p>${item.description}</p>

                <div class="price">
                    ₹ ${item.price}
                </div>

                <div class="quantity">

                    <button onclick="decrease(${item.id})">-</button>

                    <span>${item.quantity}</span>

                    <button onclick="increase(${item.id})">+</button>

                </div>

            </div>

            <button
                class="delete-btn"
                onclick="removeItem(${item.id})">

                Delete

            </button>

        </div>

        `;

    });

    grandTotal.innerHTML = "₹ " + total;

})
.catch(error => console.log(error));

}

// Quantity Increase
function increase(id){

    fetch(`http://127.0.0.1:8000/cart/increase/${id}`,{
        method:"PUT"
    })
    .then(()=>loadCart());

}


// Quantity Decrease
function decrease(id){

    fetch(`http://127.0.0.1:8000/cart/decrease/${id}`,{
        method:"PUT"
    })
    .then(()=>loadCart());

}


// Delete Item
function removeItem(id){

    fetch(`http://127.0.0.1:8000/cart/${id}`,{
        method:"DELETE"
    })
    .then(()=>loadCart());

}

loadCart();