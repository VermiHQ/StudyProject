from django.forms import ModelForm, Form, CharField, ImageField
from .models import Dish


class DishForm(ModelForm):
    class Meta:
        model = Dish
        fields = ['title', 'type', 'ingredients', 'recipe', 'image']
        image = ImageField()

class SearchForm(Form):
    query = CharField()
