from django.urls import path, re_path, include
from . import views
from django.views.decorators.csrf import csrf_exempt


app_name = 'Manage'

urlpatterns = [
    path('', views.order_form, name='order_form'),
    path('subs/', views.subs, name='subs'),
    path('new_order/', views.new_order, name='new_order'),
    path('choise_brand/', views.choise_brand, name='choise_brand'),
    path('save_order/', views.save_order, name='save_order'),
    path('calc_price/', views.calc_price, name='calc_price'),
]
