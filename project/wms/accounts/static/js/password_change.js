var password = document.getElementById("password")
var confirm = document.getElementById("confirm")
var form = document.getElementById("changeform")
const alert = document.getElementById('alert-msg');

form.addEventListener("submit" , function(){
     event.preventDefault();
    if( password.value == ""){
         alert.textContent = "please fill all the blanks"
         alert.style.display = "block";
    }
    if (password.value === confirm.value){
        submit_ps(password.value)
    }else{
         alert.textContent = "Passwords not Matched !"
         alert.style.display = "block";
    }
})
function submit_ps(password){
    const pathParts = window.location.pathname.split("/");
    const token = pathParts[pathParts.length - 1]; 

    fetch("/submit_password" , {
        "method":"POST",
        "headers":{
            "Content-Type":"application/json",
            "X-CSRFToken":document.getElementsByName("csrfmiddlewaretoken")[0].value,
            
        },
        "body": JSON.stringify({"password":password , "token":token}),
        "credentials": "include"
    }).then(response => response.json())
    .then(data =>{
        if (data.status){
             
        alert.textContent = "Passwords changed succssfully"
        window.location.href = "/login"
         alert.style.display = "block";
        }else if (data.href == "here"){
        alert.textContent = data.reason
         alert.style.display = "block";
        }else{
            window.location.href = "/login"
        }
    })
}