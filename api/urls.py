from rest_framework.routers import DefaultRouter

from api.views import (UserModelViewSet, StoreModelViewSet,
                       ProductModelViewSet, OrderModelViewSet,
                       SupplyModelViewSet)

router = DefaultRouter()
router.register('users', UserModelViewSet, basename='users')
router.register('stores', StoreModelViewSet, basename='stores')
router.register('products', ProductModelViewSet, basename='products')
router.register('supplies', SupplyModelViewSet, basename='supplies')
router.register('orders', OrderModelViewSet, basename='orders')

urlpatterns = [

]

urlpatterns.extend(router.urls)
