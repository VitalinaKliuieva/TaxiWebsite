from rest_framework import serializers

from .models import (
    Car,
    DriverLead,
    InvestorLead
)


class CarSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Car

        fields = "__all__"


class DriverSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = DriverLead

        fields = "__all__"


class InvestorSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = InvestorLead

        fields = "__all__"
