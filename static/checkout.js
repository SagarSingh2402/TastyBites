function placeOrder(){

    fetch("http://127.0.0.1:8000/order/place",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            customer_name: document.getElementById("name").value,
            phone: document.getElementById("phone").value,
            address: document.getElementById("address").value,
            payment_method: document.getElementById("payment").value

        })

    })

    .then(res => res.json())

    .then(data => {

        if(data.message === "Cart is Empty"){
            alert("Cart is Empty");
            return;
        }

        window.location.href =
        `/order/success?order_id=${data.order_id}&total=${data.total}`;

    })

    .catch(err => {

        console.error(err);
        alert("Something went wrong!");

    });

}