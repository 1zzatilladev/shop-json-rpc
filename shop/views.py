from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django.core.cache import cache

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer






class MyPaginator(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'limit'
    max_page_size = 100


class ProductListCreateApiView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = MyPaginator
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['price']


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = MyPaginator

    def get_queryset(self):
        value = cache.get('category_list')
        if value:
            return value
        data = super().get_queryset()
        cache.set('category_list', data, 900)
        return data

# swagger, redoc












class ProductApiView(APIView):

    def get(self, request, pk=None):
        category_id = request.GET.get("category_id", None)
        product_name = request.GET.get("product_name", None)
        limit = int(request.GET.get("limit", 10))
        page = int(request.GET.get("page", 0))
        if pk:
            products = Product.objects.filter(id=pk)
        else:
            products = Product.objects.all()
        if category_id:
            products = products.filter(category__id=category_id)
        if product_name:
            products = products.filter(name__icontains=product_name)
        if limit and page:
            products = products[page:limit]

        products_ser = ProductSerializer(products, many=True)
        data = {
            "message": "ok",
            "products": products_ser.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        ser = ProductSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
        data = {
            "message": "product created successfully",
            "product": ser.data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        product = Product.objects.get(id=pk)
        ser = ProductSerializer(product, data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
        data = {
            "message": "product updated successfully",
            "product": ser.data
        }
        return Response(data, status=status.HTTP_202_ACCEPTED)

    def patch(self, request, pk=None):
        product = Product.objects.get(id=pk)
        ser = ProductSerializer(product, data=request.data, partial=True)
        if ser.is_valid(raise_exception=True):
            ser.save()
        data = {
            "message": "product updated successfully",
            "product": ser.data
        }
        return Response(data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            msg = 'product deleted successfully'
            status_code = status.HTTP_204_NO_CONTENT
        except Product.DoesNotExist:
            msg = "Product not found"
            status_code = status.HTTP_404_NOT_FOUND
        data = {
            "message": msg,
        }
        return Response(data, status=status_code)




