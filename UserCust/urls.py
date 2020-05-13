from django.urls import path, re_path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'UserCust'

urlpatterns = [
    path('reg_form/', views.MyRegisterFormView.as_view(), name="register"),
]
