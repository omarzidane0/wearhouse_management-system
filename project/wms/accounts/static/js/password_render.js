var email = document.getElementById("email")
var form = document.getElementById("resetform")
var alert = document.getElementById("alert-msg")
form.addEventListener("submit" , function(){
    event.preventDefault()
    if (email.value == ""){
        alert.textContent = "please fill all the blanks"
        alert.style.display = "block";
    }else{
      send_link(email.value)
    }
})

function send_link(email){
    fetch("reset_post" , {
        "method": "POST",
        "headers":{
        "Content-Type":"application/json",
        "X-CSRFToken":document.getElementsByName("csrfmiddlewaretoken")[0].value,
       
        },
        "body": JSON.stringify({"email" : email}),
        "credentials": "include"
    }).then(response => response.json())
    .then(data =>{
        if(data.status == true){
        alert.style.color = "#6ee7b7"
        alert.textContent = data.reason
        alert.style.display = "block";
        }else{
         alert.textContent = data.reason
         alert.style.display = "block";
        }
    })
}