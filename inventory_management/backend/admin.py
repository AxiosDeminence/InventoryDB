from django.contrib import admin

# Register your models here.

from .models import User, Character, Item

admin.site.register(User)
admin.site.register(Character)
admin.site.register(Item)