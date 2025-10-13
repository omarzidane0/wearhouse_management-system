   const colorsContainer = document.getElementById('colors-container');
    const addColorBtn = document.getElementById('add-color-btn');
    const previewOutput = document.getElementById('preview-output');
    const botForm = document.getElementById('bot-form');
   const section_c = document.getElementById('section-container');
   let colors_g = []
get_info()    
function get_info(){
  try{
  fetch('/inventory/s_info' , {
    'method':'GET',
    'headers' : {
        'Content-Type' : 'Application/json',
        'X-CSRFToken':getCookie('csrftoken'),
    }
  }).then(resp =>resp.json())
  .then(data =>{
    console.log(data)
    create_inputs(data.companys , 'الشركة' ,'company' )
    create_inputs(data.categorys , 'النوع','bot_type')
  })}
  catch(err){

  }
  try{
          fetch("/inventory/color_c" , {
        "method" : "GET",
        "headers":{
            "Content-Type":"Applications/json",
            "X-CSRFToken":document.getElementsByName("csrfmiddlewaretoken")[0].value, 
        }}).then( response => response.json())
        .then(data =>{
          //  console.log(data.colors)
            colors_g.push(data.colors)
        })}catch(err){

        }
        console.log(colors_g)
}
function create_inputs(data,name , tag){
    const input = document.createElement("select")
    input.name = tag
    const label = document.createElement('label')
    label.textContent = name
  data.forEach(elm =>{
    const option  = document.createElement("option")
    option.value = elm.name
    option.textContent = elm.name
    input.appendChild(option)
  })
  section_c.appendChild(label)
  section_c.appendChild(input)
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


    function refreshPreview() {
      const botData = {
        name: botForm.bot_name.value || '',
        type: botForm.bot_type.value || '',
        company: botForm.company.value || '',
        imageName: botForm.image.files[0]?.name || '',
        colors: []
      };
console.log("bot name is " + botData.name)
      colorsContainer.querySelectorAll('.color-section').forEach(cs => {
        const colorName = cs.querySelector('select[name="color[]"]').value || '';
        const sizes = [];
        cs.querySelectorAll('.size-section').forEach(sz => {
          sizes.push({
            size: sz.querySelector('input[name="size[]"]').value || '',
            quantity: sz.querySelector('input[name="quantity[]"]').value || ''
          });
        });
        botData.colors.push({ color: colorName, sizes });
      });
      console.log(botData.colors)
      console.log(botData.colors.length)
    //  if (!botData.name || botData.colors.length === 0) {
      //  console.log("there is no name or colors")
        //previewOutput.innerHTML = 'لا توجد بيانات بعد.';
       // return;
      //}

      let html = `<div style="font-weight:bold; margin-bottom:8px; color:#444">${botData.name} — ${botData.type} — ${botData.company}</div>`;
      if (botData.imageName) html += `<div style="margin-bottom:8px">صورة: ${botData.imageName}</div>`;

      botData.colors.forEach(c => {
        html += `<div style="margin-bottom:6px; color:#555"><strong>لون:</strong> ${c.color}</div>`;
        c.sizes.forEach(s => {
          html += `<div class="product-card"> <img src="https://via.placeholder.com/60?text=${encodeURIComponent(c.color)}" alt="img"> <div>حجم: ${s.size} — كمية: ${s.quantity}</div></div>`;
        });
      });

      previewOutput.innerHTML = html;
      return botData
    }

    function createColorSection(buttonText = 'إضافة حجم') {
      const colorDiv = document.createElement('div');
      colorDiv.className = 'color-section';

      const colorInput = document.createElement('select');
      
      colorInput.name = 'color[]';
      colorInput.placeholder = 'اللون';
      colorInput.required = true;

      colors_g[0].forEach(elm =>{
        const option = document.createElement("option")
        option.value = elm.name
        option.textContent = elm.name
        colorInput.appendChild(option)
      })


      const addSizeBtn = document.createElement('button');
      addSizeBtn.type = 'button';
      addSizeBtn.className = 'add-btn';
      addSizeBtn.textContent = buttonText;

      const removeColorBtn = document.createElement('button');
      removeColorBtn.type = 'button';
      removeColorBtn.className = 'remove-btn';
      removeColorBtn.textContent = 'حذف اللون';

      const sizesContainer = document.createElement('div');
      sizesContainer.className = 'sizes-container';

      colorDiv.appendChild(colorInput);
      colorDiv.appendChild(addSizeBtn);
      colorDiv.appendChild(sizesContainer);
      colorDiv.appendChild(removeColorBtn);

      addSizeBtn.addEventListener('click', () => {
        const sizeDiv = document.createElement('div');
        sizeDiv.className = 'size-section';
        const sizeInput = document.createElement('input');
        sizeInput.type = 'text';
        sizeInput.name = 'size[]';
        sizeInput.placeholder = 'الحجم';
        sizeInput.required = true;

        const quantityInput = document.createElement('input');
        quantityInput.type = 'number';
        quantityInput.name = 'quantity[]';
        quantityInput.placeholder = 'الكمية';
        quantityInput.required = true;

        const removeSizeBtn = document.createElement('button');
        removeSizeBtn.type = 'button';
        removeSizeBtn.className = 'remove-btn';
        removeSizeBtn.textContent = 'حذف الحجم';

        removeSizeBtn.addEventListener('click', () => { sizeDiv.remove(); refreshPreview(); });
        sizeInput.addEventListener('input', refreshPreview);
        quantityInput.addEventListener('input', refreshPreview);

        sizeDiv.appendChild(sizeInput);
        sizeDiv.appendChild(quantityInput);
        sizeDiv.appendChild(removeSizeBtn);
        sizesContainer.appendChild(sizeDiv);
        refreshPreview();
      });

      colorInput.addEventListener('input', refreshPreview);
      removeColorBtn.addEventListener('click', () => { colorDiv.remove(); refreshPreview(); });

      colorsContainer.appendChild(colorDiv);
      refreshPreview();
    }

    addColorBtn.addEventListener('click', () => createColorSection('إضافة حجم'));


    botForm.addEventListener('submit', (e) => { e.preventDefault();
    
    const result = refreshPreview();
    console.log("testing")
    console.log(result)
     alert('تم حفظ البوت بنجاح!'); 
    post_data(result)
    
    });

    function post_data(data){
        if (data == null){
            return;
        }
        const formdata = new FormData();
        const fileInput = document.querySelector("#image");
        formdata.append("image", fileInput.files[0]);
        console.log(data)
        formdata.append("data" , JSON.stringify(data))
        fetch("/inventory/a_product_post/",{
            'method':'POST',
            'headers':{
                 'X-CSRFToken':getCookie('csrftoken'),
            },
            'body': formdata
        }).then(response=>response.json())
        .then(data =>{
            console.log(data)
        })
    }