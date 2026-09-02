from django.contrib import admin

from .models import Car, DriverLead, InvestorLead


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("name", "transmission", "fuel_type", "seats", "price", "price_period", "is_available", "created_at")
    list_editable = ("is_available", "price")
    list_filter = ("transmission", "fuel_type", "is_available")
    search_fields = ("name", "badge")
    ordering = ("-created_at",)


@admin.register(DriverLead)
class DriverLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number", "created_at", "contacted")
    list_editable = ("contacted",)
    list_filter = ("contacted", "created_at")
    search_fields = ("name", "email", "phone_number")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(InvestorLead)
class InvestorLeadAdmin(admin.ModelAdmin):
    list_display = (
        "name", "car_brand", "car_model", "car_year", "offer_type",
        "expected_price", "created_at", "contacted",
    )
    list_editable = ("contacted",)
    list_filter = ("offer_type", "contacted", "created_at")
    search_fields = ("name", "email", "phone_number", "car_brand", "car_model")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)