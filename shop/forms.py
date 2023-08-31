from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.urls import reverse_lazy

from shop.models import Flowers, Versions


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class FlowersForm(StyleFormMixin,forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_action = reverse_lazy('shop:flowers_list/')


    class Meta:
        model = Flowers
<<<<<<< HEAD
        exclude = ('date_of_creation', 'last_modified_date', 'employee')
=======
        exclude = ('date_of_creation', 'last_modified_date',)
>>>>>>> origin/main

    def clean_name(self):
        bad = {'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
               'радар'}
        cleaned_data = self.cleaned_data['name']
        words_name = cleaned_data.lower().split()
        if bad & set(words_name):
            raise forms.ValidationError(f'У нас запрешеннно использовать слова - {bad}')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Versions
        fields = '__all__'

    def clean_active_is(self):
        cleaned_data = self.cleaned_data['active_is']
        # print(cleaned_data)
        # print(self.instance.product.version_set.filter(indicator=True).exclude(id=self.instance.id).exists())

        if cleaned_data and self.instance.bouquet.versions_set.filter(active_is=True).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError(f'Может существовать только одна активная версия.')

        return cleaned_data
