from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import DriverLeadForm, InvestorLeadForm
from .models import Car


def home(request):
    context = {"cars": Car.objects.filter(is_available=True)[:6]}
    return render(request, "home.html", context)


def for_drivers(request):
    context = {"cars": Car.objects.filter(is_available=True)[:6]}
    return render(request, "for_drivers.html", context)


def for_investors(request):
    return render(request, "for_investors.html")


def contacts(request):
    """Renders the Contacts page with both (empty) forms — submission happens via fetch()."""
    context = {
        "driver_form": DriverLeadForm(),
        "investor_form": InvestorLeadForm(),
    }
    return render(request, "contacts.html", context)


@require_POST
def submit_driver_lead(request):
    form = DriverLeadForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "errors": form.errors}, status=400)


@require_POST
def submit_investor_lead(request):
    form = InvestorLeadForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "errors": form.errors}, status=400)