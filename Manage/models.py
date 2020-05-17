from django.db import models
from UserCust.models import CustomUser

# Create your models here.

class ServCategory(models.Model):
    name = models.CharField('Категория', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория услуг'
        verbose_name_plural = 'Категории услуг'


class ServSubcategory(models.Model):
    name = models.CharField('Подкатегория', max_length=255)
    serv_category = models.ForeignKey(ServCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Цена", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория услуг'
        verbose_name_plural = 'Подкатегории услуг'


class ProductBrand(models.Model):
    name = models.CharField('Производитель оборудования', max_length=255)
    contacts = models.CharField('Контакты', max_length=255, null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель оборудования'
        verbose_name_plural = 'Производители оборудования'


class Product(models.Model):
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Оборудование', max_length=255)
    price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Цена", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'

class Client(models.Model):
    fio = models.CharField('ФИО', max_length=255)
    sfera = models.CharField('Сфера деятельности', max_length=255)
    name_org = models.CharField('Название организации', max_length=255)
    tel = models.CharField('Телефон', max_length=255)
    email = models.CharField('Email', max_length=255)
    web = models.CharField('Вебсайт', max_length=255)
    empl_quant = models.CharField('Общее число сотрудников', max_length=255)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Order(models.Model):
    STATUS = (('wait', 'Ожидает рассмотрения'), ('work', 'В работе'), ('compl', 'Завершена'),)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Менеджер')
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Сотрудник', related_name='worker', null=True)
    services = models.ManyToManyField(ServSubcategory, verbose_name='Услуги', blank=True)
    products = models.ManyToManyField(Product, verbose_name='Оборудование', blank=True)
    client_coment = models.TextField('Комментарйи клиента', null=True, blank=True, max_length=1000)
    manager_coment = models.TextField('Комментарий менеджера', null=True, blank=True)
    begin = models.DateField('Начало проекта', null=True)
    end = models.DateField('Окончание проекта', null=True)
    ins_date = models.DateField('Время подачи', null=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS, default='wait')

    def __str__(self):
        return self.client.fio

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
