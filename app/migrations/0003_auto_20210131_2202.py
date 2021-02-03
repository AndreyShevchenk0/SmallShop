# Generated by Django 3.0.8 on 2021-01-31 20:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210131_2033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Кошик', 'verbose_name_plural': 'Кошик'},
        ),
        migrations.AlterModelOptions(
            name='cartproduct',
            options={'verbose_name': 'Кошик з продуктами', 'verbose_name_plural': 'Кошик з продуктами'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категорію', 'verbose_name_plural': 'Категорії'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Покупця', 'verbose_name_plural': 'Покупці'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Замовлення покупця', 'verbose_name_plural': 'Замовлення покупців'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукти'},
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='app.Cart', verbose_name='кошик'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Адреса'),
        ),
        migrations.AlterField(
            model_name='order',
            name='buying_type',
            field=models.CharField(choices=[('self', 'Самовывоз'), ('delivery', 'Доставка')], default='self', max_length=100, verbose_name='Тип замовлення'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Cart', verbose_name='Кошик'),
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментаріі до замовлення'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата замовлення'),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Фамілія'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата отримання замовлення'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'Нове замовлення'), ('in_progress', 'Замовлення в обробці'), ('is_ready', 'Замовлення готове'), ('completed', 'Замовлення виконане')], default='new', max_length=100, verbose_name='Статус замовлення'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, verbose_name='наіменування'),
        ),
    ]