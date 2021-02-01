# Generated by Django 3.0.8 on 2021-02-01 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210131_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFeatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_key', models.CharField(max_length=100, verbose_name='ключ характеристики')),
                ('feature_name', models.CharField(max_length=255, verbose_name='наіменування характеристики')),
                ('postfix_for_value', models.CharField(blank=True, help_text='наприклад для характеристик "години роботи" до значення можно добавити постфикс "годин", як результ "10 годин"', max_length=20, null=True, verbose_name='постфикс для значення')),
                ('use_in_filter', models.BooleanField(default=False, verbose_name='використовувати в філтраціі товарів в шаблоні')),
                ('filter_type', models.CharField(choices=[('radio', 'Радіокнопка'), ('checkbox', 'Чекбокс')], default='checkbox', max_length=20, verbose_name='тип фільтра')),
                ('filter_measure', models.CharField(help_text='Одиниця виміру для конкретного фільтру.Наприклад "Частота процесора (Ghz)"', max_length=50, verbose_name='Одинядля виміру для фільтра')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category', verbose_name='категорія')),
            ],
        ),
        migrations.CreateModel(
            name='ProductFeaturesValidators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_value', models.CharField(max_length=255, unique=True, verbose_name='Значення характеристики')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category', verbose_name='категория')),
                ('feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ProductFeatures', verbose_name='Характеристика')),
            ],
        ),
    ]
