from django.shortcuts import get_object_or_404
from functools import reduce
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from product.models import Product
from .serializers import CartItemSerializer
from .models import CartItem


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_cart(request):

    cart_items = CartItem.objects.filter(user=request.user)
    total_price = reduce(lambda acc, item: acc + item.price, cart_items, 0)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response({'cart_total': total_price, "cart_items": serializer.data, "cart_count": cart_items.count()})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, pk):
    user = request.user
    try:
        product = Product.objects.get(id=pk)
        cart_item = CartItem.objects.filter(product=product, user=user).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.price = cart_item.price * cart_item.quantity
            cart_item.save()
            serializer = CartItemSerializer(cart_item, many=False)
            return Response({'details': 'Cart item updated'})
        else:
            cart = CartItem.objects.create(
                user=user,
                product=product,
                price=product.price,
            )
            return Response({'details': "Item added to cart"})

    except Product.DoesNotExist:
        return Response({'error': 'No such product found'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, pk):
    try:
        cart_item = CartItem.objects.filter(
            user=request.user, product=pk).first()

        if cart_item:
            if cart_item.quantity == 1:
                cart_item.delete()
            else:
                cart_item.quantity -= 1  
                cart_item.save()  
            return Response({"details": 'item removed'})            
        else:
            return Response({"error": 'no such item in cart'})
    except:
        return Response({'error': "No such product in cart"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items.delete()

    return Response({'details': 'cart cleared'})