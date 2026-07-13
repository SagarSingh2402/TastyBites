document.getElementById("registerForm")
.addEventListener("submit", function(e){

    e.preventDefault();

    fetch("http://127.0.0.1:8000/auth/register",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            name:document.getElementById("name").value,

            email:document.getElementById("email").value,

            password:document.getElementById("password").value

        })

    })

    .then(res=>res.json())

    .then(data=>{
        if(data.message=="User Registered Successfully"){

            window.location="/auth/login";

        }else{

           alert(data.message);

        }

       

    })

    .catch(err=>console.log(err));

});