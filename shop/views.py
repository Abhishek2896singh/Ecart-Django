from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
from .models import Product,Contact,Orders,OrderUpdate
import json
from django.views.decorators.csrf import csrf_exempt
# from .paytm import Checksum
# MERCHANT_KEY = 'Your-Merchant-Key-Here'

# Create your views here.
def index(request):
    allProds=[]
    catprods=Product.objects.values('category','id')
    cats={item['category']for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n= len(prod)
        nSlides= n//4 + ceil((n/4) + (n//4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allProds }
    return render(request,"shop/index.html", params)


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
    

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<3:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)



def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method=="POST":
        print(request)
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, "shop/contact.html")
    

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates,order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except :
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)


    return render(request, 'shop/Products.html', {'product':product[0]})

def checkout(request):
    if request.method=="POST":
        
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        amount=request.POST.get('amount', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')

        order = Orders(items_json= items_json, name=name,amount=amount, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank=True
        id=order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
        # param_dict={
        #     'MID': 'Your-Merchant-Id-Here',
        #         'ORDER_ID': str(order.order_id),
        #         'TXN_AMOUNT': str(amount),
        #         'CUST_ID': email,
        #         'INDUSTRY_TYPE_ID': 'Retail',
        #         'WEBSITE': 'WEBSTAGING',
        #         'CHANNEL_ID': 'WEB',
        #         'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')



@csrf_exempt
def handlerequest(request):
    return HttpResponse("Done")
    