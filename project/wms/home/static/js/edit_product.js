let color_list = []
let companies = []
let category = []
let product_colors = []
let product_id = window.location.pathname.split("/").filter(Boolean).pop()
let loading = document.getElementById('loading')

console.log(product_id)
        let select_category = document.getElementById("productCategory")
        let select_company = document.getElementById('productCompany')
start()
async function start(){
  loading.style.display = 'block';
let info = await get_info();
console.log(info)
  await fetchColors();         // استنى الألوان تتعبّى
  await grap_data();           // استنى البيانات
  await grap_product_colors(); // استنى تحميل الألوان الخاصة بالمنتج
  await grap_product_sizes();
    loading.style.display = 'none';
}
async function get_info(){
        return await fetch("/inventory/s_info",{
        method:'GET',
        headers:{ 'X-CSRFToken':getCookie('csrftoken') },
    })
    .then(response => response.json())
    .then(data =>{
        data['categorys'].forEach(element => {
           
          let option = document.createElement("option")
          option.value = element.name
          option.textContent = element.name
          select_category.appendChild(option)
        });
        data['companys'].forEach(element => {
                    let option = document.createElement("option")
          option.value = element.name
          option.textContent = element.name
          select_company.appendChild(option)
        });
            companies = data['companys']
            category = data['categorys']
            
            return data
    });
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function color(){
    return fetch("/inventory/color_c",{
        method:'GET',
        headers:{ 'X-CSRFToken':getCookie('csrftoken') },
    })
    .then(response => response.json())
    .then(data =>{
        console.log("داخل then:", data['colors']);
        return data['colors'];
    });
}
async function fetchColors() {
    color_list = await color();
    console.log("الألوان وصلت:", color_list); // ✅ تطبع مليانة
    return color_list;
}
function toggleColors() {
      const section = document.getElementById('colorsSection');
      section.style.display = section.style.display === 'none' ? 'block' : 'none';
    }

    function toggleSizes(btn) {
      const row = btn.parentElement.parentElement.nextElementSibling;
      if (row && row.classList.contains('sizesRow')) {
        row.style.display = row.style.display === 'none' ? 'table-row' : 'none';
      }
    }
async function addColor() {
  let response = await fetch(`/inventory/add_colors/${product_id}`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({})  // السيرفر هو اللي بيختار اللون
  });

  let data = await response.json(); // ← مهم جدًا await

  if (data.status) {
    const table = document.querySelector('#colorsTable tbody');
    const newColor = document.createElement('tr');

    let optionsHTML = "";
    color_list.forEach(color => {
      optionsHTML += `<option value="${color.name}">${color.name}</option>`;
    });

    newColor.innerHTML = `
      <td>
        <select id='colors' color_id="${data.color_id}">
          ${optionsHTML}
        </select>
      </td>
      <td>
        <button class='show' onclick='toggleSizes(this)'>عرض المقاسات</button>
        <button class='add' onclick='saveColor(this)' color_id=${data.color_id}>💾 حفظ</button>
      </td>
    `;

    const newSizes = document.createElement('tr');
    newSizes.classList.add('sizesRow');
    newSizes.style.display = 'none';
    newSizes.innerHTML = `
      <td colspan='2'>
        <table class='sizesTable'>
          <thead>
            <tr><th>المقاس</th><th>الكمية</th><th>خيارات</th></tr>
          </thead>
          <tbody color_id=${data.color_id}></tbody>
        </table>
        <button class='add' onclick='addSize(this) color_id=${data.color_id}'>➕ إضافة مقاس</button>
      </td>
    `;

    table.appendChild(newColor);
    table.appendChild(newSizes);
    let select_color = document.querySelector(`select[color_id="${data.color_id}"]`)
    console.log(data.color)
    select_color.value = data.color
  } else {
    console.log(data.reason);
    alert(`فشل في إضافة اللون\n${data.reason}`);
  }
}

  async  function addSize(btn) {
      const tbody = btn.previousElementSibling.querySelector('tbody');
      const newRow = document.createElement('tr');
      let color_id_s = btn.getAttribute('color_id')
      console.log(color_id_s)
      let response = await fetch(`/inventory/add_sizes/${color_id_s}`)
      let data = await response.json();
      if (data.status){
        console.log(data)
      newRow.innerHTML = `<td><input type='text' placeholder='مقاس' value=${data.size}></td><td><input type='number' value='${data.quantity}'></td><td><button class='add'size_id=${data.ps_id} onclick='saveSize(this)'>💾 حفظ</button></td>`;
      tbody.appendChild(newRow);}
        else{
          alert(data.reason)
        }
    }

    function saveProduct() {
      try{
      const name = document.getElementById('productName').value;
      const category = document.getElementById('productCategory').value;
      const company = document.getElementById('productCompany').value;
      console.log('تم حفظ المنتج:', { name, category, company });
      fetch(`/inventory/product/${product_id}` , {
        'method':'POST',
        'headers':{
             'X-CSRFToken':getCookie('csrftoken') 
        },
        'body':JSON.stringify({'name':name , 'category':category, 'company':company}) 
           }).then(response => response.json())
           .then(data =>{
            if(data.status){
              alert(" تم حفظ بيانات المنتج")
            }else{
              console.log(data)
              alert(`error saving the product ! ${data.reason}` )
            }
           })
          
          }
      catch{
        alert("error saving the product !")
      }
    }

    async function saveColor(btn) {
      const row = btn.parentElement.parentElement;
      const color = row.querySelector('select').value;
      const color_id = btn.getAttribute('color_id');
      const response = await fetch(`/inventory/save_colors/${color_id}`
        ,{
          method : 'POST',
          headers:{   'X-CSRFToken':getCookie('csrftoken') },
          body: JSON.stringify({'color':color}),
           cache: "no-store"
        }
      );
      const data = await response.json();
      console.log(data);
      alert('تم حفظ اللون' +color + "  id "+color_id);
    }

    async function saveSize(btn) {
      const row = btn.parentElement.parentElement;
      const size = row.querySelector('input[type=text]').value;
      const qty = row.querySelector('input[type=number]').value;
      const size_id = btn.getAttribute('size_id');
      const response = await fetch(`/inventory/save_sizes/${size_id}`
        ,{
          method : 'POST',
          headers:{   'X-CSRFToken':getCookie('csrftoken') },
          body: JSON.stringify({'size':size , 'quantity':qty}),
           cache: "no-store"
        }
      );
      const data = await response.json();
      console.log('تم حفظ المقاس:', { size, qty });
      console.log(data)
      alert('تم حفظ المقاس');
    }

async function grap_data(){
  try{
        await fetch(`/inventory/product/${product_id}` , {
        'method':'GET',
        'headers':{
             'X-CSRFToken':getCookie('csrftoken') 
        },
         cache: "no-store"
      }).then(response => response.json())
      .then(data =>{
        let name_input = document.getElementById('productName')
        name_input.value = data.name
        select_category.value = data.category
        select_company.value = data.company
      })
  }catch{
    alert("error while grapping product data")
  }
}
async function grap_product_colors(){
  console.log("dammm")
 
            await fetch(`/inventory/product_colors/${product_id}` , {
        'method':'GET',
        'headers':{
             'X-CSRFToken':getCookie('csrftoken') 
        },
        cache: "no-store"
      }).then(response => response.json())
      .then(data =>{
        console.log(data)
        product_colors = data.result
          if (data.status){
              const table = document.querySelector('#colorsTable tbody');
              data.result.forEach(element => {
      const newColor = document.createElement('tr');
    let optionsHTML = "";
    color_list.forEach(color => {
        optionsHTML += `<option value="${color.name}">${color.name}</option>`;
    });

    // بعدين تحط الـ options في الـ innerHTML
    newColor.innerHTML = `
    <td>
        <select id='colors' color_id=${element.id}>
        ${optionsHTML}
        </select>
    </td>
    <td>
        <button class='show' onclick='toggleSizes(this)'>عرض المقاسات</button>
        <button class='add' onclick='saveColor(this)' color_id=${element.id}>💾 حفظ</button>
    </td>
    `;
        color_list.forEach(element => {
            console.log(element.name)
            const option = document.createElement('option')         
        });
        const colors = document.getElementById('colors')
      const newSizes = document.createElement('tr');
      newSizes.classList.add('sizesRow');
      newSizes.style.display = 'none';
      newSizes.innerHTML = `<td colspan='2'><table class='sizesTable'><thead><tr><th>المقاس</th><th>الكمية</th><th>خيارات</th></tr></thead><tbody color_id=${element.id}></tbody></table><button class='add' color_id=${element.id} onclick='addSize(this)'>➕ إضافة مقاس</button></td>`;
      newColor.setAttribute('color_id', element.id);
      table.appendChild(newColor);
      table.appendChild(newSizes);
      let select_color = document.querySelector(`select[color_id="${element.id}"]`)
      select_color.value = element.color
              });
          }else{

          }
      })

}
async function grap_product_sizes() {
  console.log(product_colors)
  if (!product_colors){
    alert('there is no colors for this product')
  }else{
  for (const element of product_colors) {
    const response = await fetch(`/inventory/get_sizes/${element.id}`,{
        cache: "no-store"
    });
    const data = await response.json();
    let tbody = document.querySelector(`tbody[color_id="${element.id}"]`)
    // تعامل مع الداتا هون
    console.log(data);
    if (data.result){
    data.result.forEach(elem => {
      const newRow = document.createElement('tr');
      newRow.innerHTML = `<td><input type='text' placeholder='مقاس' value=${elem.size}></td><td><input type='number' value='${elem.quantity}'></td><td><button class='add'size_id=${elem.id} onclick='saveSize(this)'>💾 حفظ</button></td>`;
      tbody.appendChild(newRow);
    });}
  }}
}