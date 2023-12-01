from rest_framework import serializers
from .models import Category, Review, Product, Tag
from rest_framework.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name product_count product_list'.split()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'category_name review_list title description price tag_list'.split()


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


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    description = serializers.CharField(required=False, max_length=128)
    price = serializers.IntegerField(min_value=0)
    category_id = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_tags(self, tags):
        tags_from_db = Tag.objects.filter(id__in=tags)
        if len(tags) != len(tags_from_db):
            tags_from_db_set = set(tags_from_db.values_list("id", flat=True))
            not_found_tags = list(set(tags).difference(tags_from_db_set))
            raise ValidationError(f"Tag(s) do not exist: {not_found_tags}")
        return tags

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist')
        return category_id


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    product_id = serializers.IntegerField()
    stars = serializers.IntegerField(min_value=1, max_value=5)

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist')
        return product_id
