#from PIL import Image
from django.forms import ModelChoiceField, ModelForm#, ValidationError
#from django import forms
from django.contrib import admin
#from django.utils.safestring import mark_safe
from .models import *


class SmartphoneAdminForm(ModelForm):
    """ проверка флажка в sd для смартфона от ошибки при снятии флажка """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and not instance.sd:
            self.fields['sd_volume_max'].widget.attrs.update({
                'readonly': True, 'style': 'background: lightgray;'
            })

    # метод очистки
    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volume_max'] = None
        return self.cleaned_data


# class NotebookAdminForm(ModelForm):
#     """ Минимальна та максимальна вага зображення """
#     # MIN_RESOLUTION = (400, 400)
#     # MAX_RESOLUTION = (800, 800) # перенесли в модель Product
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['image'].help_text = mark_safe\
#             ("""<span style="color:red; font-size:14px">Завантажуйте зображення ''з розумом {}*{}''</span>"""
#                                                    .format(*Product.MIN_RESOLUTION))

    # def clean_images(self):
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #     min_height, min_width = Product.MIN_RESOLUTION
    #     max_height, max_width = Product.MAX_RESOLUTION
    #     if image.size > Product.MAX_IMAGE_SIZE:
    #         raise ValidationError('Розмір зображення завеликий скоротіть до 3 МB.')
    #     if img.height < min_height or img.width < min_width:
    #         raise ValidationError('Завантажене зображення замале')
    #     if img.height > max_height or img.width > max_width:
    #         raise ValidationError('Завантажене зображення завелике')
    #     return Image


class NotebookAdmin(admin.ModelAdmin):

    #form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    change_form_template = 'admin.html'  # свой шаблон
    form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)