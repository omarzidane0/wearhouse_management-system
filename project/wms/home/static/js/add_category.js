    const form = document.getElementById("categoryForm");
    const input = document.getElementById("categoryInput");
    const list = document.getElementById("categoryList");
    const loading = document.getElementById('loading');
var alert_msg = document.getElementById("alert-msg-ph")
    firs_fetch()
    function firs_fetch(){
        loading.style.display = "block"
        fetch("/inventory/category_c" , {
        "method" : "GET",
        "headers":{
            "Content-Type":"Applications/json",
            "X-CSRFToken":document.getElementsByName("csrfmiddlewaretoken")[0].value, 
        }}).then( response => response.json())
        .then(data =>{
            if(data.status){
                console.log(data.category)
        data.category.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item['name'];
        list.appendChild(li);
        input.value = "";})
                loading.style.display = "none";
            }else{
                loading.status.display = "none";
            }
        })
    }


    form.addEventListener("submit", function(e) {
      e.preventDefault();
        loading.style.display = "block"
        const value = input.value.trim();
        fetch("/inventory/category_c" , {
        "method" : "POST",
        "headers":{
            "Content-Type":"Applications/json",
            "X-CSRFToken":document.getElementsByName("csrfmiddlewaretoken")[0].value, 
        },
        'body': JSON.stringify({'value':value})
    }).then( response => response.json())
      .then(data =>{
        if(data.status){
            loading.style.display = "none";
            const li = document.createElement("li");
        li.textContent = value;
        list.appendChild(li);
        input.value = "";
        alert_msg.textContent = "added success !!"
        alert_msg.style.display = "block";

        }else if(data.href != null){
            window.location.href = "/"+data.href
        }else{
                    alert_msg.textContent = data.reason
        alert_msg.style.display = "block";
            loading.style.display = "none";
        }
      })
    });

