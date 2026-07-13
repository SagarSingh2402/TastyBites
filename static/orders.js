fetch("http://127.0.0.1:8000/order/history/data")

.then(response=>response.json())

.then(data=>{

const container=document.getElementById("orders-container");

container.innerHTML="";

if(data.length==0){

container.innerHTML=`

<div class="empty">

No Orders Found

</div>

`;

return;

}

data.forEach(order=>{

container.innerHTML+=`

<div class="order-card">

<h2>Order #${order.id}</h2>

<div class="row">

<strong>Customer</strong>

<span>${order.customer_name}</span>

</div>

<div class="row">

<strong>Phone</strong>

<span>${order.phone}</span>

</div>

<div class="row">

<strong>Total</strong>

<span>₹ ${order.total_amount}</span>

</div>

<div class="row">

<strong>Payment</strong>

<span>${order.payment_method}</span>

</div>

<div class="row">

<strong>Status</strong>

<span>${order.status}</span>

</div>

<div class="row">

<strong>Date</strong>

<span>${new Date(order.created_at).toLocaleString()}</span>

</div>

<div class="status">

${order.status}

</div>

</div>

`;

});

})

.catch(error=>console.log(error));