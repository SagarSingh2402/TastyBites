document.getElementById("menuForm")

.addEventListener("submit",function(e){

e.preventDefault();

fetch("http://127.0.0.1:8000/admin/menu",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

item_name:document.getElementById("item_name").value,

price:Number(document.getElementById("price").value),

category:document.getElementById("category").value,

description:document.getElementById("description").value,

image:document.getElementById("image").value

})

})

.then(res=>res.json())

.then(data=>{


window.location="/admin/manage-menu";

})

.catch(err=>console.log(err));

});