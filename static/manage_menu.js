fetch("http://127.0.0.1:8000/admin/menu")

.then(response=>response.json())

.then(data=>{

const table=document.getElementById("menu-table");

table.innerHTML="";

data.forEach(item=>{

table.innerHTML += `
<tr>

<td>${item.id}</td>

<td>
<img src="${item.image}">
</td>

<td>${item.item_name}</td>

<td>₹ ${item.price}</td>

<td>${item.category}</td>

<td>

<button
class="edit"
onclick="editItem(${item.id})">
Edit
</button>

<button
class="delete"
onclick="deleteItem(${item.id})">
Delete
</button>

</td>

</tr>
`;
});

})

.catch(error=>console.log(error));

function editItem(id){

window.location=`/admin/edit-menu/${id}`;

}

function deleteItem(id){

    console.log("Delete clicked:", id);

    if(confirm("Are you sure?")){

        fetch(`http://127.0.0.1:8000/admin/menu/${id}`,{

            method:"DELETE"

        })

        .then(res=>res.json())

        .then(data=>{

            

            location.reload();

        })

        .catch(err=>console.log(err));

    }

}