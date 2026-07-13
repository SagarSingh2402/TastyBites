const params = new URLSearchParams(window.location.search);

document.getElementById("order-id").innerHTML =
params.get("order_id");

document.getElementById("total").innerHTML =
params.get("total");