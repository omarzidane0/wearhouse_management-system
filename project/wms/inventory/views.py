from django.shortcuts import render
from accounts.decorators import session_req_json
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
import json
import random
from inventory.models import Category , Color , Company , Product , ProductColor , ProductStock
from django.db.models import F, Value
from django.db.models.functions import Lower, Replace
# Create your views here.
@session_req_json
def categorys_control(request):
    user = request.user_obj
    if user.role.can_add_products:
        if request.method == "POST":
            category = json.loads(request.body.decode("utf-8")).get("value")
            if len(category.strip()) == 0:
                return  JsonResponse({'status':False , 'reason':' please fill all the blanks !'})
            if Category.objects.filter(name=category).exists():
                return JsonResponse({'status':False , 'reason':' category already exist !'})
            else:
                try:
                    Category.objects.create(name=category)
                    return JsonResponse({'status':True , "reason":"added !!"})
                except:
                    return JsonResponse({'status':False , "reason":"unexpected error !"})
        else:
            categorys = list(Category.objects.all().values("name"))
            return JsonResponse({'status':True , 'category':categorys})
    else:
        return JsonResponse({'status':False , 'reason':"don't have a premssion" , 'href':f'{user.role.home_href}'})


@session_req_json
def colors_control(request):
    user = request.user_obj
    if user.role.can_add_products:
        if request.method == "POST":
            color = json.loads(request.body.decode("utf-8")).get("value")
            if len(color.strip()) == 0:
                return  JsonResponse({'status':False , 'reason':' please fill all the blanks !'})
            if Color.objects.filter(name=color).exists():
                return JsonResponse({'status':False , 'reason':' color already exist !'})
            else:
                try:
                    Color.objects.create(name=color)
                    return JsonResponse({'status':True , "reason":"added !!"})
                except:
                    return JsonResponse({'status':False , "reason":"unexpected error !"})
        else:
            colors = list(Color.objects.all().values("name"))
            return JsonResponse({'status':True , 'colors':colors})
    else:
        return JsonResponse({'status':False , 'reason':"don't have a premssion" , 'href':f'{user.role.home_href}'})

@session_req_json
def company_control(request):
   
    user = request.user_obj
    if user.role.can_add_products:
        if request.method == "POST":
            company = json.loads(request.body.decode("utf-8")).get("value")
            if len(company.strip()) == 0:
                return  JsonResponse({'status':False , 'reason':' please fill all the blanks !'})
            if Company.objects.filter(name=company).exists():
                return JsonResponse({'status':False , 'reason':' company already exist !'})
            else:
                try:
                    Company.objects.create(name=company)
                    return JsonResponse({'status':True , "reason":"added !!"})
                except:
                    return JsonResponse({'status':False , "reason":"unexpected error !"})
        else:
            Companys = list(Company.objects.all().values("name"))
            return JsonResponse({'status':True , 'Companys':Companys})
    else:
        return JsonResponse({'status':False , 'reason':"don't have a premssion" , 'href':f'{user.role.home_href}'})



def product_list(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 2)
    search_status = request.GET.get('search_status')
    search_val = request.GET.get('search_val')
    print(search_status)
    print(search_val)
    if not search_status:
        products = Product.objects.all()
        print('false')
    else:
        print('true')
        search = search_val  # المستخدم كتب الاسم بأي شكل
        normalized_search = "".join(search.split()).lower()  # نحذف الفراغات ونصغّر الحروف -> "johndoe"
        products = Product.objects.annotate(
            name_normalized=Lower(Replace(F('name'), Value(' '), Value('')))
        ).filter(name_normalized__contains=normalized_search)
    
    
    paginator = Paginator(products, per_page)
    page_obj = paginator.get_page(page_number)

    data = {
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "current_page": page_obj.number,
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category.name,
                "company": p.company.name,
                "img":str(p.image_url)
            }
            for p in page_obj
        ]
    }
    return JsonResponse(data, safe=False)
@session_req_json
def get_products(request):
    user = request.user_obj
    if user.role.can_create_orders:
        return product_list(request)    
    else:
        return JsonResponse({'status':False , 'reason':"don't have a premssion" , 'href':f'{user.role.home_href}'})
@session_req_json
def get_info(request):
    user = request.user_obj
    if user.role.can_create_orders:
        data ={
            "companys": list(Company.objects.all().values("name")),
            "categorys": list(Category.objects.all().values("name"))
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'status':False , 'reason':"don't have a premssion" , 'href':f'{user.role.home_href}'})


@session_req_json
def add_product(request):
    ##### remmember to secure it
    if request.user_obj.role.can_add_products:
        image = request.FILES.get("image")
        data = json.loads(request.POST.get("data"))
        fields = [data['name'], data['type'], data['company'], data['imageName'] ]
        print(data)
        if any(v is None or str(v).strip() == '' for v in fields):
            return JsonResponse({'status':False , 'reason':'please fill all the fields'})
        try:
            product = Product.objects.create(name=data['name'] , category=Category.objects.filter(name=data['type']).first() , company=Company.objects.filter(name=data['company']).first(),image_url=image)
        except Exception as e:
            return JsonResponse({'status':False , 'reason':f'faild to add the product {e}'})
        
        if len(data['colors']) > 0:
            for color in data['colors']:
                if color['color'].strip() == "":
                    return JsonResponse({'status':False , 'reason':'product created , faild to add the color'})
                try:
                    product_c = ProductColor.objects.create(product=product , color=Color.objects.filter(name=color['color']).first())
                except:
                    return JsonResponse({'status':False , 'reason':f'product created faild to add the color {color}'})
                if color['sizes'] != None:
                    for s in color['sizes']:
                        if s['size'].strip() == '' or s['quantity'].strip() == '':
                            return JsonResponse({'status':False , 'reason':f'product created , faild to add the sizes to the color {color}'})
                        try:
                            p_s = ProductStock.objects.create(product=product , color=product_c,size=s['size'],quantity=s['quantity'])
                            return JsonResponse({'status':True , 'reasaon':'product added !!'})
                        except:
                            return JsonResponse({'status':False ,'reason':'product added faild to add the sizes'})

        
        return JsonResponse({'status':True , 'reason':'product added'})
    else:
        return JsonResponse({'status':False , 'reason':"don't have a premssion" , 'href':f'{request.user_obj.role.home_href}'})


@session_req_json
def productq(request , id):
    user = request.user_obj
    if not user.role.can_add_products:
        return JsonResponse({'status':False , 'reason':"you don't have the premmison"})
    product_q = Product.objects.filter(id=id)
    if not product_q.exists():
        return JsonResponse({'status':False , 'reason':'Wrong product id'})
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        company = data.get('company')
        category = data.get('category')
        fields = [name , company , category ]
        if any(v is None or str(v).strip() == '' for v in fields):
            return JsonResponse({'status':False , 'reason':'please fill all the fields'})
        company_d = Company.objects.filter(name=company)
        if not company_d.exists():
            return JsonResponse({'status':False , 'reason':'Wrong Company , Company Doesnt Exist'})
        category_d = Category.objects.filter(name=category)
        if not category_d.exists():
            return JsonResponse({'status':False , 'reason':'Wrong Category , Category Doesnt Exist'})
        
        if product_q.exists():
            p = product_q.first()
            p.name = name
            p.company = company_d.first()
            p.category = category_d.first()
            p.save()
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False , 'reason':"Product Doesn't exist"})
    else:
        p = product_q.first()
        return JsonResponse({'status':True , 'name':p.name , 'category':p.category.name , 'company':p.company.name})


@session_req_json
def product_colors(request , id):
    user = request.user_obj
    if not user.role.can_add_products:
        return JsonResponse({'status':False , 'reason':"you don't have the premmison"})
    product = Product.objects.filter(id=id)
    if not product.exists():
        return JsonResponse({'status':False , 'reason':"product doesn't exist .. wrong id"})
    product_c = ProductColor.objects.filter(product=product.first())
    if not product_c.exists():
        return JsonResponse({'status':False , 'reason':"there is no colors"})
    data = []
    for p in product_c:
        dic = {
            'color': p.color.name,
            'id':p.id
        }
        data.append(dic)
    return JsonResponse({'status':True , 'result':data})


@session_req_json
def get_sizes(request , id):
    user = request.user_obj
    if user.role.can_add_products:
        product_c = ProductColor.objects.filter(id=id)
        if not product_c.exists():
            return JsonResponse({'status':False , 'reason':'Wrong Color ID'})
        p_c = product_c.first()
        ps = ProductStock.objects.filter(color=p_c)
        if not ps.exists():
            return JsonResponse({'status':False , 'reason':'there is no sizes for this color'})
        sizes = []
        for size in ps:
            data = {
                'id':size.id,
                'size':size.size,
                'quantity':size.quantity
            }
            sizes.append(data)
        return JsonResponse({'status':True ,'result':sizes})

    
@session_req_json
def save_size(request , id):
    user = request.user_obj
    if not user.role.can_add_products:
        return JsonResponse({'status':False , 'reason':"you don't have the premmison"})
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        s = data.get('size')
        q = data.get('quantity')
        if len(s.strip())==0 or not q:
            return JsonResponse({'status':False , 'reason':"please fill all the blanks"})
        size = ProductStock.objects.filter(id=id)
        if not size.exists():
            return JsonResponse({'status':False , 'reason':'Wrong ID THERE IS NO SIZE'})
        p_size = size.first()
        p_size.size=s 
        p_size.quantity=q 
        p_size.save()
        return JsonResponse({'status':True , 'reason':'size update'})


@session_req_json
def save_color(request , id):
    user = request.user_obj
    if not user.role.can_add_products:
        return JsonResponse({'status':False , 'reason':"you don't have the premmison"})
    pc = ProductColor.objects.filter(id=id)
    if not pc.exists():
        return JsonResponse({'status':False , 'reason':'Wrong ID THERE IS NO Color'})
    
    data = json.loads(request.body.decode('utf-8'))
    color_q = Color.objects.filter(name=data.get('color'))
    if not color_q.exists():
        return JsonResponse({'status':False , 'reason':' THERE IS NO Color with this naem'})
    pc_c = pc.first()
    pc_c.color = color_q.first()
    pc_c.save()
    print(pc_c.color.name)
    pc_c.refresh_from_db()
    print(pc_c.color.name)
    return JsonResponse({'status':True , 'reason':'Color Update'})
    

@session_req_json
def add_color(request, id):
    user = request.user_obj
    if not user.role.can_add_products:
        return JsonResponse({'status': False, 'reason': "you don't have permission"})

    product_ = Product.objects.filter(id=id).first()
    if not product_:
        return JsonResponse({'status': False, 'reason': 'Wrong Product ID'})

    # كل الألوان
    all_colors = Color.objects.all()

    # الألوان اللي المنتج هذا أصلاً مضافها
    existing_colors = ProductColor.objects.filter(product=product_).values_list('color_id', flat=True)

    # الألوان اللي لسه مش مضافة
    available_colors = all_colors.exclude(id__in=existing_colors)

    if not available_colors.exists():
        return JsonResponse({'status': False, 'reason': 'no remaining colors to add'})

    # اختار لون واحد (عشوائي)
    color_to_add = random.choice(list(available_colors))

    # أضفه للمنتج
    p = ProductColor.objects.create(product=product_, color=color_to_add)

    return JsonResponse({
        'status': True,
        'reason': 'added one available color',
        'color': color_to_add.name,
        'color_id': p.id
    })

@session_req_json
def add_size(request,id):
    user = request.user_obj
    if not user.role.can_add_products:
        return JsonResponse({'status': False, 'reason': "you don't have permission"})
    product_color = ProductColor.objects.filter(id=id)
    if not product_color.exists():
        return JsonResponse({'status':False , 'reason':'wrong product color id'})
    try:
        s=1
        q=1
        ps = ProductStock.objects.create(product=product_color.first().product , color=product_color.first() , size=s , quantity=q)
        return JsonResponse({'status':True , 'ps_id':ps.id , 'size':s , 'quantity':q})
    except:
        return JsonResponse({'status':False , 'reason':'error while adding the size'})


    

    
