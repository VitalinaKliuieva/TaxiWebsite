from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Car(models.Model):
    """A single vehicle in the fleet — shown in the home/for-drivers carousel."""

    class Transmission(models.TextChoices):
        AUTOMATIC = "automatic", _("Automatic")
        MANUAL = "manual", _("Manual")

    class FuelType(models.TextChoices):
        PETROL = "petrol", _("Petrol")
        DIESEL = "diesel", _("Diesel")
        HYBRID = "hybrid", _("Hybrid")
        ELECTRIC = "electric", _("Electric")

    class PricePeriod(models.TextChoices):
        DAY = "/day", _("Per day")
        WEEK = "/week", _("Per week")
        MONTH = "/month", _("Per month")

    name = models.CharField(max_length=100, help_text=_("e.g. Toyota Corolla 2022"))
    transmission = models.CharField(max_length=20, choices=Transmission.choices, default=Transmission.AUTOMATIC)
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices, default=FuelType.PETROL)
    seats = models.PositiveSmallIntegerField(default=4)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    price_period = models.CharField(max_length=10, choices=PricePeriod.choices, default=PricePeriod.WEEK)
    badge = models.CharField(max_length=30, blank=True, help_text=_("Optional label, e.g. 'New' or 'Popular'"))
    image = models.ImageField(upload_to="cars/", blank=True, null=True)
    is_available = models.BooleanField(default=True, help_text=_("Untick to hide from the site without deleting it"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return self.image.url if self.image else ""

    @property
    def detail_url(self):
        return f"/cars/{self.pk}/"


class DriverLead(models.Model):
    """A submission from the driver contact form."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    contacted = models.BooleanField(default=False, help_text="Tick once someone on the team has followed up")
    notes = models.TextField(blank=True, help_text="Internal notes — not shown to the applicant")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Driver lead"

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"


class InvestorLead(models.Model):
    """A submission from the investor contact form."""

    class OfferType(models.TextChoices):
        SELL = "sell", _("Sell the car")
        RENT = "rent", _("Rent it out through Taxi Partner")

    name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=30)
    email = models.EmailField()
    date_of_registration = models.DateField(
        default=timezone.now,
        help_text="Date the offer was submitted / preferred registration date",
    )
    offer_type = models.CharField(max_length=10, choices=OfferType.choices)
    car_brand = models.CharField(max_length=60)
    car_model = models.CharField(max_length=60)
    car_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1980), MaxValueValidator(2100)]
    )
    expected_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    contacted = models.BooleanField(default=False, help_text="Tick once someone on the team has followed up")
    notes = models.TextField(blank=True, help_text="Internal notes — not shown to the applicant")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Investor lead"

    def __str__(self):
        return f"{self.name} — {self.car_brand} {self.car_model} ({self.get_offer_type_display()})"