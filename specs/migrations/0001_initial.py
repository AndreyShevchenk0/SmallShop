# Generated by Django 3.0.8 on 2021-02-01 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0005_auto_20210201_2348'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=100, verbose_name='імя характеристіки')),
                ('feature_filter_name', models.CharField(max_length=50, verbose_name='Імя для фільтра')),
                ('unit', models.CharField(blank=True, max_length=50, null=True, verbose_name='одиниця виміру')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'характеристика категорії',
                'verbose_name_plural': 'характеристика категоріі',
                'unique_together': {('category', 'feature_name', 'feature_filter_name')},
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Значення')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='specs.CategoryFeature', verbose_name='Характеристика')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'характеристики товару',
                'verbose_name_plural': 'характеристикі товару',
            },
        ),
        migrations.CreateModel(
            name='FeatureValidator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_feature_value', models.CharField(max_length=100, verbose_name='валідне значення')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category', verbose_name='категорія')),
                ('feature_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='specs.CategoryFeature', verbose_name='ключ характеристики')),
            ],
            options={
                'verbose_name': 'валідатор для характеристики',
                'verbose_name_plural': ' валідатор для характеристики',
            },
        ),
    ]
