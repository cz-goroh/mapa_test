from django.shortcuts import render
from UserCust.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from .forms import RegForm
# Create your views here.



# Вариант регистрации на базе класса FormView
class MyRegisterFormView(FormView):
    form_class = RegForm
    success_url = "/admin/"
    template_name = "UserCust/reg_form.html"

    def form_valid(self, form):
        form.save()
        return super(MyRegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)

# def
