from rest_framework.routers import DefaultRouter

from api.views import UserModelViewSet, StoreModelViewSet, ProductModelViewSet, \
    OrderModelViewSet

router = DefaultRouter()
router.register('users', UserModelViewSet)
router.register('stores', StoreModelViewSet)
router.register('products', ProductModelViewSet)
router.register('orders', OrderModelViewSet)


urlpatterns = [

]

urlpatterns.extend(router.urls)