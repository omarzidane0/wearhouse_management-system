
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("addUserForm");
  const alert_msg = document.getElementById("alert-msg");
     get_roles(alert_msg)
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
      username: form.username.value.trim(),
      email: form.email.value.trim(),
      password: form.password.value,
      phone: form.phone.value.trim(),
      role: form.role.value
    };
    if (!payload.username ||!payload.email || !payload.password||!payload.phone||!payload.role){
      alert_msg.style.display = "block";
      alert_msg.textContent =  "please fill all the blanks !";
    }else{
           try {
      const res = await fetch("/add_users_post/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
            "X-CSRFToken":document.getElementsByName("csrfmiddlewaretoken")[0].value,
          "Accept": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      console.log("Response data:", data);

      if (!res.ok) {
        alert_msg.style.display = "block";
        alert_msg.textContent =  "unexpected error";
        return;
      }

      if(data.status == false){
              alert_msg.style.display = "block";
      alert_msg.textContent = data.reason ;
      }else{
      alert_msg.style.display = "block";
      alert_msg.textContent = data.message || "user added successfully";}
      form.reset();

    } catch (err) {
      alert_msg.style.display = "block";
      alert_msg.textContent = "error connecting to the server";
      console.error("Fetch error:", err);
    }
    }
 
  });
});

async function get_roles(alert_msg){
               try {
      const res = await fetch("/get_roles/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
            "X-CSRFToken":document.getElementsByName("csrfmiddlewaretoken")[0].value,
          "Accept": "application/json"
        }
      });

      const data = await res.json();

      console.log("Response data:", data);

      if (!res.ok) {
        alert_msg.style.display = "block";
        alert_msg.textContent =  "unexpected error";
        return;
      }
      var user_select = document.getElementById("role_select")
      data.roles.forEach(item => {
    const option = document.createElement("option");
    option.value = item.role;  // القيمة اللي ترسل للباك اند
    option.textContent = item.role;  // النص المعروض للمستخدم
    user_select.appendChild(option);
     });
    
      form.reset();

    } catch (err) {
    }
}