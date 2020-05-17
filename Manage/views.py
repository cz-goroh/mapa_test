from django.shortcuts import render
import datetime
from decimal import Decimal
from django.db.models import Sum
from django.http import  HttpResponse, HttpResponseRedirect, JsonResponse

from .models import *
# Create your views here.

def new_worker(request):
    n_us = CustomUser.objects.create_user(
        request.POST['username'],
        '',
        request.POST['password'],
        )
    n_us.is_staff=True
    n_us.save()
    return HttpResponseRedirect('/admin/')

def calc_price(request):
    serv_l = request.POST['serv_l'].split(',')
    print(request.POST['serv_l'])
    try:
        serv_pr = ServSubcategory.objects.filter(pk__in=serv_l).aggregate(Sum('price'))['price__sum'] or 0
    except:
        serv_pr = 0
    prod_l = request.POST['prod_l'].split(',')
    try:
        prod_pr = Product.objects.filter(pk__in=prod_l).aggregate(Sum('price'))['price__sum'] or 0
    except:
        prod_pr = 0
    price = serv_pr + prod_pr
    return JsonResponse({'price': price})

def save_order(request):
    obj = Order.objects.get(pk=request.POST['this_obj'])
    obj.manager = request.user
    obj.worker = CustomUser.objects.get(id=request.POST['worker'])
    obj.manager_coment = request.POST['manager_coment']
    obj.status = 'work'
    servs_list = []
    for k,v in request.POST.items():
        if k.split('_')[0] == 'serv':
            servs_list.append(v)
    servs = [s for s in ServSubcategory.objects.filter(pk__in=servs_list)]
    prods_list = []
    for k,v in request.POST.items():
        if k.split('_')[0] == 'prod':
            prods_list.append(v)
    prods = [p for p in Product.objects.filter(pk__in=prods_list)]
    print(prods)
    obj.save()
    obj.services.clear()
    # print(obj.services.all())
    obj.services.add(*servs)
    obj.products.clear()
    obj.products.add(*prods)
    obj.save()
    return HttpResponseRedirect('/admin/Manage/order/')

def choise_brand(request):
    brand = Product.objects.get(pk=request.POST['prod']).brand
    return JsonResponse({'brand_id': f'#brand_{brand.id}'})

def new_order(request):
    p = request.POST
    try:
        client = Client.objects.get(fio=request.POST['fio'])
    except:
        client = Client(
            fio=p['fio'],
            sfera=p['sfera'],
            name_org=p['name_org'],
            tel=p['tel'],
            email=p['email'],
            web=p['web'],
            empl_quant=p['empl_quant'],
        )
        client.save()

    begin_dat_split = request.POST['begin'].split('-')
    begin_date = datetime.date(
        int(begin_dat_split[0]),
        int(begin_dat_split[1]),
        int(begin_dat_split[2]),
    )
    end_dat_split = request.POST['end'].split('-')
    end_date = datetime.date(
        int(end_dat_split[0]),
        int(end_dat_split[1]),
        int(end_dat_split[2]),
    )
    n_ord = Order(
        client=client,
        begin=begin_date,
        end=end_date,
        client_coment=p['coment'],
        ins_date = datetime.date.today()
    )
    n_ord.save()
    n_ord.services.add(ServSubcategory.objects.get(pk=p['serv_subcategory']))
    return HttpResponse('Спасибо за заявку, мы с Вами свяжемся')

def subs(request):
    subs = [ {'id': s.id, 'name':s.name}
        for s in ServSubcategory.objects.filter(serv_category=request.POST['cat'])]
    return JsonResponse({'subs': subs})

def order_form(request):
    cats = ServCategory.objects.all()
    subcats = ServSubcategory.objects.filter(serv_category=cats[0])
    q={
        'cats': cats,
        'subcats': subcats,
    }
    return render(request, 'Manage/order_form.html', q)
