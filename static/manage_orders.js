fetch("http://127.0.0.1:8000/admin/orders")

.then(response=>response.json())

.then(data=>{

const table=document.getElementById("orders-table");

table.innerHTML="";

data.forEach(order=>{

table.innerHTML+=`

<tr>

<td>${order.id}</td>

<td>${order.customer_name}</td>

<td>${order.phone}</td>

<td>₹ ${order.total_amount}</td>

<td>${order.payment_method}</td>

<td>

<select id="status-${order.id}">

<option ${order.status=="Pending"?"selected":""}>Pending</option>

<option ${order.status=="Preparing"?"selected":""}>Preparing</option>

<option ${order.status=="Out For Delivery"?"selected":""}>Out For Delivery</option>

<option ${order.status=="Delivered"?"selected":""}>Delivered</option>

<option ${order.status=="Cancelled"?"selected":""}>Cancelled</option>

</select>

</td>

<td>

<button onclick="updateStatus(${order.id})">

Update

</button>

</td>

</tr>

`;

});

});

function updateStatus(id){

    const status = document.getElementById(`status-${id}`).value;

    fetch(`http://127.0.0.1:8000/admin/orders/${id}`,{

        method:"PUT",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            status:status
        })

    })

    .then(res=>res.json())

    .then(data=>{

        

        location.reload();

    })

    .catch(err=>console.log(err));

}