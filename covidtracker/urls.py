from django.urls import path
from . import views

from .views import StateView, DistrictView, EachStateView

urlpatterns = [
    path("", views.covid_state, name="covid-home"),
    path("district", views.covid_district, name="district"),
    path("<str:s_name>/", views.each_state, name="city"),
    path("api/states/", StateView.as_view(), name="state-api"),
    path("api/districts/", DistrictView.as_view(), name="district-api"),
    path("api/districts/<str:s_name>/", views.EachStateView, name="state_cities-api"),
    path(
        "api/districts/<str:s_name>/<str:c_name>/",
        views.EachCityCaseView,
        name="state_city_case_api",
    ),
]
