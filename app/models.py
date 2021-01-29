# import sys
# from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes. fields import GenericForeignKey
from django.urls import reverse
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from io import BytesIO

User = get_user_model()

def get_models_for_count(*model_names):
    return [models.Count(model_names)for model_name in model_names]

# функция преобразующая все модели Products
# аналог get_absolut_url
def get_product_url(obj, viewname):
    ct_model = obj.__class__.meta.model_name
    return  reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass

# 1 Category
# 2 Product
# 3 CartProduct
# 4 Cart
# 5 Order
# 6 Customer
# 7 Specifications

class LatestProductsManager:
    """ менеджер модели """
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
    """ обьект менеджера модели """
    object = LatestProductsManager()


class CategoryManager(models.Manager):
    """ млдель категорий менеджер """

    CATEGORY_NAME_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Смартфони': 'smartphone__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models =get_models_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*models).values())
        return [dict(name=c['name'], slug=c['slug'], count=c[self.CATEGORY_NAME_COUNT_NAME[c['name']]])for c in qs]


class Category(models.Model):
    """ модель категорii """

    name = models.CharField(max_length=255, verbose_name='имя категорii')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name


class Product(models.Model):
    """  абстрактна модель продукту для подальшого наслідування """

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)
    MAX_IMAGE_SIZE = 3145728

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

    # def save(self, *args, **kwargs):
    #     """ Пренудительне обрізання зображення """
    #     # основной вариант
    #     image = self.image
    #     img = Image.open(image)
    #     new_img = img.convert('RGB')
    #     resized_new_img = new_img.resize((200, 200), Image.ANTIALIAS)
    #     filestream = BytesIO()
    #     resized_new_img.save(filestream, 'JPEG', quality=90)
    #     filestream.seek(0)
    #     name = '{}.{} '.format(*self.image.name.split('.'))
    #     print(self.image.name, name)
    #     self.image = InMemoryUploadedFile(
    #         filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
    #     )
    #     super().save(*args, **kwargs)


        # 2-й вариант
        # min_height, min_width = self.MIN_RESOLUTION
        # max_height, max_width = self.MAX_RESOLUTION
        # if img.height < min_height or img.width < min_width:
        #     raise MinResolutionErrorException('Завантажене зображення замале')
        # if img.height > max_height or img.width > max_width:
        #     raise MaxResolutionErrorException('Завантажене зображення завелике')
        #super().save(*args, **kwargs)
        #return Image


class CartProduct(models.Model):
    """ модель связку покупок покупця та корзини """

    user = models.ForeignKey('Customer', verbose_name='покупець', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    #product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='загальна вартість')

    def __str__(self):
        return 'Продукт: {} (для корзини)'.format(self.content_object.title)


class Cart(models.Model):
    """ модель корзини """

    owner = models.ForeignKey('Customer', verbose_name='власник', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_car')
    total_products = models.PositiveIntegerField(default=0)  # для коректного отображения товара в корзине
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='загальна вартість')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    """ модель покупця """

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
    """ Модель ноутбука
    клас наслідник від моделі Продукту """

    diagonal = models.CharField(max_length=255, verbose_name='диагонал')
    display_type = models.CharField(max_length=255, verbose_name='итп дисплея')
    processor_freg = models.CharField(max_length=255, verbose_name='процесор')
    ram = models.CharField(max_length=255, verbose_name='оперативная память')
    video = models.CharField(max_length=255, verbose_name='видео карта')
    time_without_charge = models.CharField(max_length=255, verbose_name='акумулятор')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

class Smartphone(Product):
    """ Модель смартфону
    клас наслідник від моделі Продукту"""

    diagonal = models.CharField(max_length=255, verbose_name='диагонал')
    display_type = models.CharField(max_length=255, verbose_name='итп дисплея')
    resolution = models.CharField(max_length=255, verbose_name='разрешение екрана')
    accum_volume = models.CharField(max_length=255, verbose_name=' обьем батареі')
    ram = models.CharField(max_length=255, verbose_name='оперативная память')
    video = models.CharField(max_length=255, verbose_name='видео карта')
    sd = models.BooleanField(default=True, verbose_name='наявність SD карти')
    sd_volume_max = models.CharField(max_length=255, null=True, blank=True,
                                     verbose_name='максимальная вбудована память')
    main_cam_mp = models.CharField(max_length=255, verbose_name='главная касера')
    front_cam_mp = models.CharField(max_length=255, verbose_name='фронтальная камера')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')
