from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Product, ProductImages
from .serializer import ProductSerializer, ProductImagesSerializer
from .filters import ProductsFilter

# Create your views here.


@api_view(['GET'])
def get_products(request):

    filterset = ProductsFilter(
        request.GET, queryset=Product.objects.all().order_by('id'))
    resPerPage = 2
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serialize = ProductSerializer(queryset, many=True)
    return Response({
        "count": filterset.qs.count(),
        "resPage": resPerPage,
        "products": serialize.data})


@api_view(['GET'])
def get_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serialize = ProductSerializer(product, many=False)
    return Response({"product": serialize.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        product = Product.objects.create(**data, user=request.user)
        serializer = ProductSerializer(product, many=False)
        return Response({"product": serializer.data})
    else:
        return Response(serializer.errors)


@api_view(['POST'])
def upload_product_images(request):

    data = request.data
    files = request.FILES.getlist('images')

    images = []
    for f in files:
        image = ProductImages.objects.create(
            product=Product(data['product']), image=f)
        images.append(image)

    serializer = ProductImagesSerializer(images, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):

    product = get_object_or_404(Product, id=pk)

    if(request.user != product.user):
        return Response({'error': "only the owner of this account can edit this"}, status=status.HTTP_403_FORBIDDEN)
    
    product.name = request.data['name']
    product.description = request.data['description']
    product.brand = request.data['brand']
    product.price = request.data['price']
    product.stock = request.data['stock']

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response({"product": serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:
        return Response({'error': "only the owner of this account can delete this"}, status=status.HTTP_403_FORBIDDEN)
    args = {'product': pk}
    images = ProductImages.objects.filter(**args)

    for i in images:
        i.delete()

    product.delete()
    return Response({'details': "Product is deleted"}, status=status.HTTP_200_OK)
