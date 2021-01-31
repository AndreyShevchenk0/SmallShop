from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """ модель категорii """

    name = models.CharField(max_length=255, verbose_name='имя категорii')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'Категорії'  # -обьявления
        verbose_name = 'Категорію'  # -обьявление


class Product(models.Model):
    """ модель продукту для подальшого наслідування """

    category = models.ForeignKey(Category, verbose_name='категорii', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='наіменування')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='зображення')
    description = models.TextField(verbose_name='опис', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='цiна')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'Продукти'
        verbose_name = 'Продукт'


class CartProduct(models.Model):
    """ модель связку покупок покупця та корзини """

    user = models.ForeignKey('Customer', verbose_name='покупець', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='кошик', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='загальна вартість')

    def __str__(self):
        return 'Продукт: {} (для кошика)'.format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Кошик з продуктами'
        verbose_name = 'Кошик з продуктами'


class Cart(models.Model):
    """ модель кошика """

    owner = models.ForeignKey('Customer', null=True, verbose_name='власник', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_car')
    total_products = models.PositiveIntegerField(default=0)  # для коректного отображения товара в корзине
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='загальна вартість')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Кошик'
        verbose_name = 'Кошик'


class Customer(models.Model):
    """ модель покупця """

    user = models.ForeignKey(User, verbose_name='користувач', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='номер телефона')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='адреса')
    orders = models.ManyToManyField('Order', related_name='related_customer', verbose_name='Замовлення покупця')

    def __str__(self):
        return 'Покупець: {} {}'.format(self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name_plural = 'Покупці'
        verbose_name = 'Покупця'


class Order(models.Model):
    """ модель заказа покупателя """

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення в обробці'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовлення виконане')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders',
                                 on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамілія')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Кошик', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адреса', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус замовлення',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип замовлення',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментаріі до замовлення', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата замовлення')
    order_date = models.DateField(verbose_name='Дата отримання замовлення', default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Замовлення покупців'
        verbose_name = 'Замовлення покупця'
