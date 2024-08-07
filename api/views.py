from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from api.permissions import IsSeller, IsCustomer

from api.models import ApiUser, Store, Product, Order
from api.serializers import UserSerializer, StoreSerializer, ProductSerializer, \
    OrderSerializer, OrderWriteSerializer


# Create your views here.
class UserModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ApiUser.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = UserSerializer

    authentication_classes = []
    permission_classes = []


class StoreModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stores to be viewed or edited.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsSeller]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    @action(detail=True)
    def products(self, request, pk=None):
        store = get_object_or_404(Store.objects.all(), id=pk)
        store_products = store.products.filter(orders__isnull=True)
        return Response(
            ProductSerializer(store_products, many=True).data
        )


class ProductModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsSeller]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsCustomer]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return OrderWriteSerializer

        return OrderSerializer
