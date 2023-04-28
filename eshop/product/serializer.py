from rest_framework import serializers
from .models import *
from account.serializers import UserSerializer



class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    images = ProductImagesSerializer(many=True, read_only=True)
    user = UserSerializer(many=False)
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'brand',
                  'category', 'stock', "user", 'ratings', 'images')
        extra_kwargs = {
            "name": {"required": True, 'allow_blank': False},
            "description": {"required": True, 'allow_blank': False},
            "brand": {"required": True, 'allow_blank': False},
        }
