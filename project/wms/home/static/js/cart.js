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
 const sample = [
      {id:1,name:'كابل شحن سريع',desc:'طول 1.5م، متوافق مع كل الأجهزة'},
      {id:2,name:'سماعة بلوتوث',desc:'عمر البطارية 20 ساعة'},
      {id:3,name:'حافظة مرنة',desc:'مقاومة للصدمات'}
    ];

    const productsEl = document.getElementById('products');
    const productTpl = document.getElementById('productTpl');

    function renderProducts(){
      productsEl.innerHTML='';
      sample.forEach(p=>{
        const node = productTpl.content.cloneNode(true);
        node.querySelector('.title').textContent = p.name;
        node.querySelector('.desc').textContent = p.desc;
        const qInput = node.querySelector('.qVal');
        const remove = node.querySelector('.cartpage-remove');
        const thumb = node.querySelector('.cartpage-thumb');
        thumb.textContent = p.name.split(' ')[0];
        qInput.value = 1;
        remove.addEventListener('click',()=>{ node.remove(); });
        productsEl.appendChild(node);
      });
    }

   // renderProducts();
//delete button action
let del_buttons = document.querySelectorAll('.cartpage-remove'); 
del_buttons.forEach(button => {
    button.addEventListener('click', () => {
        delete_item(button.getAttribute('item-id'))
    });
});
// delete fetch
async function delete_item(val){
    let response = await fetch(`/cart/delete_item/${val}`)
    let data = await response.json()
    if(data.status){
        document.querySelector(`article[item-id="${val}"]`).remove();
    }else{
        alert(data.reason)
    }
}
//update button action with both inc and dec
let inc_btns = document.querySelectorAll('.inc')
inc_btns.forEach(inc_btn=>{
inc_btn.addEventListener('click' , ()=>{
    let p = inc_btn.parentElement
    let id = p.getAttribute('item-id')
    let qty_input = document.querySelector(`input[item-id="${id}"]`)
    let p_val = parseInt(qty_input.value)+1
    
    update_item(id , p_val , qty_input)
})
})

let dec_btns = document.querySelectorAll('.dec')
dec_btns.forEach(dec_btn =>{
dec_btn.addEventListener('click', ()=>{
        let p = dec_btn.parentElement
    let id = p.getAttribute('item-id')
    let qty_input = document.querySelector(`input[item-id="${id}"]`)
    let p_val = parseInt(qty_input.value)-1
    
    update_item(id , p_val , qty_input)
})
})

//update fetch
async function update_item(id , val , qty_input) {
    console.log(val)
    let response = await fetch(`/cart/update_item/${id}`,{
      'method':'POST',
        'headers':{
            'Content-Type': 'application/json',
            'X-CSRFToken':getCookie('csrftoken')
        },
      'body':JSON.stringify({'qty':val})
    })
    let data = await response.json()
    if (data.status){
        qty_input.value = val
    }else{
        alert(data.reason)
    }
}
    document.getElementById('cartpage-clear').addEventListener('click',()=>{
        let arl = document.querySelectorAll('article')
        arl.forEach(arl=>{
            try{
            delete_item(arl.getAttribute('item-id'))}
            catch{
                alert('error while deleting items')
            }
        })

    });
    document.getElementById('checkoutBtn').addEventListener('click',(e)=>{ e.preventDefault(); alert('تم تقديم الطلب'); });