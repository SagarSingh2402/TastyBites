fetch("http://127.0.0.1:8000/admin/stats")

.then(response => response.json())

.then(data => {

    document.getElementById("orders").innerHTML = data.orders;

    document.getElementById("users").innerHTML = data.users;

    document.getElementById("menu").innerHTML = data.menu;

    document.getElementById("revenue").innerHTML = "₹ " + data.revenue;

})

.catch(error => console.log(error));