from rest_framework.routers import DefaultRouter

from .api import (
    CarViewSet,
    DriverViewSet,
    InvestorViewSet,
)


router = DefaultRouter()


router.register(
    "cars",
    CarViewSet
)

router.register(
    "driver-requests",
    DriverViewSet
)

router.register(
    "investor-requests",
    InvestorViewSet
)


urlpatterns = router.urls