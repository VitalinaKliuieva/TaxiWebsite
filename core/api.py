from rest_framework import viewsets

from .models import (
    Car,
    DriverLead,
    InvestorLead
)

from .serializers import (
    CarSerializer,
    DriverSerializer,
    InvestorSerializer
)


class CarViewSet(
    viewsets.ModelViewSet
):

    queryset = Car.objects.all()

    serializer_class = CarSerializer

class DriverViewSet(
    viewsets.ModelViewSet
):

    queryset = DriverLead.objects.all()

    serializer_class = DriverSerializer

class InvestorViewSet(
    viewsets.ModelViewSet
):

    queryset = InvestorLead.objects.all()

    serializer_class = InvestorSerializer
