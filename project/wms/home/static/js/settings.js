console.log("test")
var currentpass = document.getElementById("current-password")
var newpass = document.getElementById("new-password")
var confirmpass = document.getElementById("confirm-password")
var email = document.getElementById("email")
var phone = document.getElementById("phone")
var email_btn = document.getElementById("submit-email")
var phone_btn = document.getElementById("submit-phone")
var alert_msg_password = document.getElementById("alert-msg-ps")
var alert_msg_phone = document.getElementById("alert-msg-ph")
var alert_msg_email = document.getElementById("alert-msg-em")
  //  #alert-msg
// FORM changepass
var pass_form = document.getElementById("changepass")
var changecontact = document.getElementById("changecontact")

pass_form.addEventListener("submit" , function(e){
    event.preventDefault()
    fetch("/change_password_settings" , {
        "method" : "POST",
        "headers":{
            "Content-Type":"Applications/json",
            "X-CSRFToken":document.getElementsByName("csrfmiddlewaretoken")[0].value, 
        },
        "body":JSON.stringify({"currentpass":currentpass.value , 
            "newpass":newpass.value,
            "confirmpass":confirmpass.value
        })
    }).then(response => response.json())
    .then(data =>{
      if(data.status == true){
        alert_msg_password.textContent = data.reason
        alert_msg_password.style.display = "block"
       
      }else if( data.status == false && data.href =="login"){
            window.location.href = "/login"
      }else{
        alert_msg_password.textContent = data.reason
        alert_msg_password.style.display = "block"
      }
    })
})

confirmpass.addEventListener("click" , function(e){

})

email_btn.addEventListener("click" , function(e){
    e.preventDefault()
    fetch("/change_email_settings" , {
        "method" : "POST",
        "headers":{
            "Content-Type":"Applications/json",
            "X-CSRFToken":document.getElementsByName("csrfmiddlewaretoken")[0].value, 
        },
        "body":JSON.stringify({"email":email.value
        })
    }).then(response => response.json())
    .then(data =>{
                    if(data.status){
                alert_msg_email.textContent = data.reason
                alert_msg_email.style.display = "block"

            }else if( data.status == false && data.href =="/login"){
                window.location.href = data.href
            }else{
                alert_msg_email.textContent = data.reason
                alert_msg_email.style.display = "block"
            }
    })
})


phone_btn.addEventListener("click" , function(e){
    e.preventDefault()
    fetch("/change_phone_settings" , {
        "method" : "POST",
        "headers":{
            "Content-Type":"Applications/json",
            "X-CSRFToken":document.getElementsByName("csrfmiddlewaretoken")[0].value, 
        },
        "body":JSON.stringify({"phone":phone.value
        })
    }).then(response => response.json())
    .then(data =>{
            if(data.status){
                alert_msg_phone.textContent = data.reason
                alert_msg_phone.style.display = "block"

            }else if( data.status == false && data.href =="/login"){
                window.location.href = data.href
            }else{
                alert_msg_phone.textContent = data.reason
                alert_msg_phone.style.display = "block"
            }
    })
})
