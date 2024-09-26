from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from api.permissions import IsSeller, IsCustomer, IsOwnerOrReadOnly

from api.models import ApiUser, Store, Product, Order, Supply
from api.serializers import UserSerializer, StoreSerializer, ProductSerializer, \
    OrderSerializer, SupplySerializer, SupplyWriteSerializer, \
    OrderWriteSerializer


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
    permission_classes = [IsAuthenticatedOrReadOnly, IsSeller, IsOwnerOrReadOnly]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    # @action(default=True)
    # def products(selfself, request, pk=None):
    #     store = get_object_or_404(Store.objects.all(), id=pk)
    #     available_products = Product.objects.filter(availability__store=store, availability__quantity__gt=0)
    #     return Response(
    #         ProductSerializer(available_products, many=True).data
    #     )

class ProductModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsSeller, IsOwnerOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SupplyModelViewSet(viewsets.ModelViewSet):
    """
       API endpoint that allows supplies to be viewed or edited.
       """
    permission_classes = [IsAuthenticatedOrReadOnly, IsSeller, IsOwnerOrReadOnly]
    queryset = Supply.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return SupplyWriteSerializer

        return SupplySerializer


class OrderModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsCustomer, IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return OrderWriteSerializer

        return OrderSerializer

    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]
    #
#
# class AvailabilityModelViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     A simple ViewSet for viewing accounts.
#     """
#     queryset = Availability.objects.all()
#     serializer_class = AvailabilitySerializer
