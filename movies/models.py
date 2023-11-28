from django.db import models
from . import const

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def product_list(self):
        return [product.title for product in self.products.all()]

    def product_count(self):
        return self.products.count()


class Product(models.Model):
    title = models.CharField(max_length=64, null=True)
    description = models.CharField(max_length=128, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products',
                                 null=True)

    def __str__(self):
        return self.title

    def review_list(self):
        return [review.text for review in self.reviews.all()]

    def category_name(self):
        return self.category.name

    def rating(self):
        if self.reviews.all().count() > 0:
            return sum([review.stars for review in self.reviews.all()]) / self.reviews.count()
        else:
            return 0





class Review(models.Model):
    text = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='reviews')
    stars = models.IntegerField(choices=const.STARS)

    def __str__(self):
        return self.text

    def product_name(self):
        return self.product.title
