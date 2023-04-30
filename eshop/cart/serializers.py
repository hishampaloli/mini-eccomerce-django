from rest_framework import serializers

from account.serializers import UserSerializer
from product.serializers import ProductSerializer

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):


    class Meta:
        model = CartItem
        fields = ('id', 'price', 'quantity', 'user', 'product')
