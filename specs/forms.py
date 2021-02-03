from django import forms
from app.models import Category

from .models import CategoryFeature#,FeatureValidator


class NewCategoryForm(forms.ModelForm):
    """ форма для створення категоріі """

    class Meta:
        model = Category
        fields = '__all__'


class NewCategoryFeatureKeyForm(forms.ModelForm):
    """ формадля створення нових характеристик """

    class Meta:
        model = CategoryFeature
        fields = '__all__'


# class FeatureValidatorForm(forms.ModelForm):
#
#     class Meta:
#         model = FeatureValidator
#         fields = ['category']
