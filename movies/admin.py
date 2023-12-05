from django.contrib import admin
from .models import Category, Review, Product, Tag
from users.models import ConfirmCode

admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(ConfirmCode)
