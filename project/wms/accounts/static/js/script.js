const btn = document.getElementById("submit")
const username = document.getElementById("user")
const password = document.getElementById("pass")
const form = document.getElementById("login-form")
const alertMsg = document.getElementById('alert-msg');


form.addEventListener("submit" , function(){
    event.preventDefault();

    if(username.value == "" || password.value == ""){
            alertMsg.style.display = 'block';
            alertMsg.textContent = "please fill all the blanks"
    }else{
        send_post_login(username.value , password.value)
    }
})

function send_post_login(username , password){

    console.log("username is " + username + " password is " + password)
    fetch("/login_post/" , {
        'method':'POST',
        "headers":{
            "Content-Type" :" application/json",
            "X-CSRFToken":document.getElementsByName("csrfmiddlewaretoken")[0].value,
        },
        "body":JSON.stringify({"username":username,"password":password})
    }).then(Response => Response.json())
    .then(data => {
        if(data.status == true){
            alertMsg.style.display = 'none';
            console.log("roting to home")
            window.location.href = "/home"
        }else{
            alertMsg.style.display = 'block';
            alertMsg.textContent = data.reason
        }
    })
}



/*
    if (username.value.length < 3 ){
        console.log("username len must be at least 3")
    }
    if (password.value.length < 8 ){
        console.log("password len must be at least 8")
    }
    on the register.js side
    */