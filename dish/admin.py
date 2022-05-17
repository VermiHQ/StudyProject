from django.contrib import admin
from .models import Dish, Type, Ingredient

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'type', 'update_date', 'user_likes', 'image')
    list_display_links = ('title', )
    filter_horizontal = ['ingredients']
    search_fields = ('title', )
    list_per_page = 10

admin.site.register(Type)
admin.site.register(Ingredient)
