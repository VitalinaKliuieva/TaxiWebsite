from django.urls import path

from . import views


urlpatterns = [
    path("contacts/", views.contacts, name="contacts"),
    path("contacts/driver/submit/", views.submit_driver_lead, name="submit_driver_lead"),
    path("contacts/investor/submit/", views.submit_investor_lead, name="submit_investor_lead"),

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "drivers/",
        views.for_drivers,
        name="for_drivers"
    ),

    path(
        "investors/",
        views.for_investors,
        name="for_investors"
    )

]