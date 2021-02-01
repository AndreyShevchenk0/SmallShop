from django.db import models


class CategoryFeature(models.Model):
    """ характеристика конкретно категоріі """

    category = models.ForeignKey('app.Category', verbose_name='категория', on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=100, verbose_name='імя характеристіки')
    feature_filter_name = models.CharField(max_length=50, verbose_name='Імя для фільтра')
    unit = models.CharField(max_length=50, verbose_name='одиниця виміру', null=True, blank=True)

    class Meta:
        unique_together = ('category', 'feature_name', 'feature_filter_name')
        verbose_name_plural = 'Характеристика категоріі'
        verbose_name = 'Характеристика категорії'

    def __str__(self):
        return f'{self.category.name} | {self.feature_name}'


class FeatureValidator(models.Model):
    """ валідатор значений для конкретной характеристики моделі """

    category = models.ForeignKey('app.Category', verbose_name='категорія', on_delete=models.CASCADE)
    feature_key = models.ForeignKey(CategoryFeature, verbose_name='ключ характеристики', on_delete=models.CASCADE)
    valid_feature_value = models.CharField(max_length=100, verbose_name='валідне значення')

    def __str__(self):
        return f"категорія {self.category.name} | Характеристика {self.feature_key.feature_name} | " \
               f"Валідне значення {self.valid_feature_value}"

    class Meta:
        verbose_name_plural = ' Валідатор для характеристик'
        verbose_name = 'Валідатор для характеристики'


class ProductFeature(models.Model):
    """  характеристикі товару """

    product = models.ForeignKey('app.Product', verbose_name='Товар', on_delete=models.CASCADE)
    feature = models.ForeignKey(CategoryFeature, verbose_name='Характеристика', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Значення')

    def __str__(self):
        return f"Товар - \"{self.product.title} | " \
               f"Характеристика - \ {self.feature.feature_name} | " \
               f"Значення - {self.value}"

    class Meta:
        verbose_name_plural = 'Характеристика товару'
        verbose_name = 'Характеристики товару'
