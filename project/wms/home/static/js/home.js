const loading = document.getElementById("loading")
const product_cont = document.getElementById("products")
const page_info = document.getElementById("page_info")
const filtersq = document.getElementById("filters")
let filtering = false;
const filter_btn = document.getElementById("fltr_btn")
const next_btn = document.getElementById("next")
const previous_btn = document.getElementById("previous")
let page_num = 1 ;
const domain = window.location.origin+"/media/";
let company = []
let categories = []
let max_pages = 0;
const query = document.getElementById('searchInput')
let bool_search = false

query.addEventListener("input" , ()=>{
  if (query.value.trim() === ""){
    bool_search = false
  }else{
    bool_search = true
  }
  product_cont.innerHTML = ""
  page_num = 1
  get_items(page_num , bool_search)
})

// جلب CSRF token من الكوكيز
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
start()
function start(){
loading.style.display = "block";
get_search_info()
get_items(page_num)}
function get_search_info(){
    fetch('/inventory/s_info',{
        "method": "GET",
        "headers": {
             'Content-Type': 'application/json',
            'X-CSRFToken':getCookie('csrftoken')
        },
    }).then(response=>response.json())
    .then(data =>{
        console.log(data)
        console.log(data.companys)
        create_filter(data.companys , "companies")
        create_filter(data.categorys , "categories")
    
    })
}
function create_filter(data , name)
{
        const div_f = document.createElement("div")
        div_f.className = "filter-options" 
        console.log(data)
        data.forEach(element => {
            console.log(element.name)
            const input = document.createElement("input")
            input.type = "checkbox"
            input.value = element.name
            const label = document.createElement("label")
            label.textContent = element.name
            label.appendChild(input)

            div_f.appendChild(label) 

                  
        })
        
                const company_div = document.createElement("div")
                company_div.id = name
                company_div.className = "filter-group"
                const filter_name = document.createElement("h4")
                filter_name.textContent = name
            company_div.appendChild(filter_name)
            company_div.appendChild(div_f)

            filtersq.appendChild(company_div)
}
function get_items(page_num , bool_search){

        page_info.textContent = String(page_num)
        console.log(bool_search + " search val "+ query.value)
    fetch(`/inventory/products?page=${page_num}&search_status=${bool_search}&search_val=${query.value}`,{
        "method": "GET",
        "headers": {
             'Content-Type': 'application/json',
            'X-CSRFToken':getCookie('csrftoken')
        },
    }).then(respones => respones.json())
    .then(data =>{
            console.log(data)
            max_pages = data.num_pages
            page_num = data.current_page
            page_info.textContent = page_num +"/" +max_pages
            data.products.forEach(element => {
                createProductCard(element)
            });
            loading.style.display = "none";
    })
}

function createProductCard(product) {
    const link = document.createElement('a')
    link.href = `${window.location.origin}/show_product/${product.id}`
    link.style.textDecoration = 'none';
    const card = document.createElement("div");
    card.className = "product-card";

    // الصورة
    const img = document.createElement("img");
    img.src = domain+product.img;
    img.alt = product.name;
    card.appendChild(img);

    // الاسم
    const h3 = document.createElement("h3");
    h3.textContent = product.name;
    card.appendChild(h3);

    // النوع
    const typeDiv = document.createElement("div");
    typeDiv.className = "product-info";
    typeDiv.textContent = `النوع: ${product.category}`;
    card.appendChild(typeDiv);


    // الشركة
    const companyDiv = document.createElement("div");
    companyDiv.className = "product-info";
    companyDiv.textContent = `الشركة: ${product.company}`;
    card.appendChild(companyDiv);


    link.appendChild(card)
    product_cont.appendChild(link)
  }

filter_btn.addEventListener("click", ()=>{
    if(filtering){
        filter_btn.style.background = "#28a745"
        filtering = false
        filter_btn.textContent = "filter"
    }else{
        filtering = true
         filter_btn.textContent = "cancel-filter"
         filter_btn.style.background = "#D11A2A"
    }
})

next_btn.addEventListener("click" , ()=>{
   if (page_num < max_pages){
    page_num ++;

    product_cont.innerHTML = ""
    get_items(page_num)}
})

previous_btn.addEventListener("click" , ()=>{
    if (page_num > 1){
        page_num--;

        product_cont.innerHTML = ""
        get_items(page_num)
    }
})