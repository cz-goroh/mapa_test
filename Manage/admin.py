from django.contrib import admin
from .models import *
from UserCust.models import CustomUser
from django.db.models import Avg, Max, Min, Sum, Count
# Register your models here.

class MyAdminSite(admin.AdminSite):
    site_header='Управление Заявками'
    site_title = 'Управление Заявками'
    index_template = 'Manage/index.html'
    # index_template = 'avtoMan/avto_dashboard.html'
    # index_template = 'avtoMan/base_admin.html'
    index_title = 'Управление Заявками'
    def each_context(self, request):
        return {
            'site_title': self.site_title,
            'site_header': self.site_header,
            'site_url' : self.site_url,
            'has_permission' : self.has_permission(request),
            'available_apps' : self.get_app_list(request),
        }

class OrderAdmin(admin.ModelAdmin):
    list_display=('id', 'client', 'v_services', 'begin', 'end', 'ins_date', 'worker', 'manager', 'client_coment', 'manager_coment', 'status', 'contacts_brands')
    change_form_template = 'Manage/ord_change_form.html'

    def contacts_brands(self, obj):
        return "\n".join([str(p.brand.contacts) + ' ' + p.brand.name for p in obj.products.all()])
    contacts_brands.short_description = 'Контактные данные поставщика'

    def v_services(self, obj):
        return "\n".join([p.name for p in obj.services.all()])
    v_services.short_description = 'Выбранные услуги'

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return Order.objects.filter(worker=request.user)
        return qs.filter(author=request.user)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = Order.objects.get(pk=object_id)
        ch_serv = ServSubcategory.objects.filter(pk__in=obj.services.all())
        ch_serv_pk = [ch.id for ch in ch_serv]
        free_servs = ServSubcategory.objects.all().exclude(pk__in=ch_serv_pk)
        ch_products = obj.products.all()
        ch_products_list = [p.id for p in ch_products]
        free_products = Product.objects.all().exclude(pk__in=ch_products_list)
        ch_brands_list = [p.brand.id for p in obj.products.all()]

        brands = ProductBrand.objects.filter(pk__in=ch_brands_list)
        free_brands = ProductBrand.objects.all().exclude(pk__in=ch_brands_list)

        try:
            serv_pr = obj.services.all().aggregate(Sum('price'))['price__sum'] or 0
        # print(serv_pr)
        except:
            serv_pr = 0
        try:
            prod_pr = obj.products.all().aggregate(Sum('price'))['price__sum'] or 0
        except:
            prod_pr = 0
        price = serv_pr + prod_pr
        extra_context = {
            'price': price,
            'ch_brands': brands,
            'ch_serv':ch_serv,
            'free_servs': free_servs,
            'workers': CustomUser.objects.filter(rules='worker'),
            'worker': obj.worker,
            'manager': obj.manager,
            'this_obj': obj,
            'ch_prods': ch_products,
            'free_products': free_products,
            'free_brands': free_brands,
        }
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


    # def save_model(self, request, obj, form, change):
    #     print('sv')
    #     if change:
    #         obj.manager = request.user
    #         obj.worker = CustomUser.objects.get(id=request.POST['worker'])
    #         obj.manager_coment = request.POST['manager_coment']
    #         servs_list = []
    #         for k,v in request.POST.items():
    #             if k.split('_')[0] == 'serv':
    #                 servs_list.append(v)
    #         print(servs_list)

        # obj.save()




class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class ServSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


my_admin = MyAdminSite(name='myadmin')

my_admin.register(ServCategory)
my_admin.register(ServSubcategory, ServSubcategoryAdmin)
my_admin.register(Product, ProductAdmin)
my_admin.register(ProductBrand)
my_admin.register(Client)
my_admin.register(Order, OrderAdmin)
