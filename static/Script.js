fetch("http://127.0.0.1:8000/menu/items")
.then(response => response.json())
.then(data => {

    const container = document.getElementById("menu-container");

    container.innerHTML = "";

    data.forEach(item => {

        container.innerHTML += `

        <div class="card">

            <img src="${item.image}" alt="${item.item_name}">

            <div class="card-body">

                <h3>${item.item_name}</h3>

                <p>${item.description}</p>

                <div class="price">₹ ${item.price}</div>

                <button
                    class="add-btn"
                    onclick="addToCart(${item.id})">

                    Add To Cart

                </button>

            </div>

        </div>

        `;

    });

});


function addToCart(menu_id){

    fetch("http://127.0.0.1:8000/cart/add",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            menu_id:menu_id,
            quantity:1

        })

    })

    .then(response=>response.json())

    .then(data=>{

        const toast=document.getElementById("toast");

        if(data.message=="Item Added To Cart"){

            toast.innerHTML="✅ Item Added To Cart";

        }else{

            toast.innerHTML="🔄 Quantity Updated";

        }

        toast.classList.add("show");

        setTimeout(()=>{

            toast.classList.remove("show");

        },2000);

    })

    .catch(error=>console.log(error));

}