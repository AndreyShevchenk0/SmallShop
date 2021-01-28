from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes. fields import GenericForeignKey

User = get_user_model()

# 1 Category
# 2 Product
# 3 CartProduct
# 4 Cart
# 5 Order
# 6 Customer
# 7 Specifications

class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model_in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__.meta.modul_name.startwith(with_respect_to),
                                  reverse=True)
        return products


class LatestProducts:

    object = LatestProductsManager()


class Category(models.Model):
    """ модель категорii """

    name = models.CharField(max_length=255, verbose_name='имя категорii')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """  абстрактна модель продукту для подальшого наслідування """
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='категорii', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='зображення')
    description = models.TextField(verbose_name='опис', null=True)  # blank = True
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='цiна')

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    """ модель связку покупок пользователя та корзини """

    user = models.ForeignKey('Customer', verbose_name='покупець', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    #product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='загальна вартість')

    def __str__(self):
        return 'Продукт: {} (для корзини)'.format(self.product.title)


class Cart(models.Model):
    """ модель корзини """

    owner = models.ForeignKey('Customer', verbose_name='власник', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_car')
    total_products = models.PositiveIntegerField(default=0)  # для коректного отображения товара в корзине
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='загальна вартість')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    """ модель користувача """

    user = models.ForeignKey(User, verbose_name='користувач', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='номер телефона')
    addres = models.CharField(max_length=255, verbose_name='адреса')

    def __str__(self):
        return 'Покупець: {} {}'.format(self.user.first_name, self.user.last_name)


# class Specifications(models.Model):
#     """ Спецификации моделi продукта """
#
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     name = models.CharField(max_length=255, verbose_name='назва товара для характеристик')
#
#     def __str__(self):
#         return 'Характеристики для товара: {}'.format(self.name)


class Notebook(Product):
    """ клас наследник """

    diagonal = models.CharField(max_length=255, verbose_name='диагонал')
    display_type = models.CharField(max_length=255, verbose_name='итп дисплея')
    processor_freg = models.CharField(max_length=255, verbose_name='процесор')
    ram = models.CharField(max_length=255, verbose_name='оперативная память')
    video = models.CharField(max_length=255, verbose_name='видео карта')
    time_without_charge = models.CharField(max_length=255, verbose_name='акумулятор')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='диагонал')
    display_type = models.CharField(max_length=255, verbose_name='итп дисплея')
    resolution = models.CharField(max_length=255, verbose_name='разрешение екрана')
    accum_volume = models.CharField(max_length=255, verbose_name=' обьем батареі')
    ram = models.CharField(max_length=255, verbose_name='оперативная память')
    video = models.CharField(max_length=255, verbose_name='видео карта')
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name='максимальная встраиваемая память')
    main_cam_mp = models.CharField(max_length=255, verbose_name='главная касера')
    front_cam_mp = models.CharField(max_length=255, verbose_name='фронтальная камера')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)


