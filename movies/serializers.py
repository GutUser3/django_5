from rest_framework import serializers
from .models import Category, Review, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name product_count product_list'.split()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'category_name review_list title description price'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text stars product_name'.split()


class ProductReviewSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = 'id title description price category reviews rating'.split()
