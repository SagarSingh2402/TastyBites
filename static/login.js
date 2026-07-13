document.getElementById("loginForm")
.addEventListener("submit", function(e){

    e.preventDefault();

    fetch("http://127.0.0.1:8000/auth/login",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            email:document.getElementById("email").value,

            password:document.getElementById("password").value

        })

    })

    .then(res=>res.json())

    .then(data=>{

        if(data.redirect){

            window.location = data.redirect;

        }else{

            alert(data.message);

        }

    })

    .catch(err=>console.log(err));

});