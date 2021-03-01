from django.shortcuts import render
from django.db.models import Avg, Count, Min, Sum
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.core import serializers

from .models import district_cases, states_cases, CasesIncrementCheck
from django.db import models
import json
import ssl
import urllib.request, urllib.error
import requests
from datetime import datetime as dt
import time

from .serializers import DistrictSerializer, StateSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


class StateView(ListAPIView):
    queryset = states_cases.objects.all()
    serializer_class = StateSerializer


class DistrictView(ListAPIView):
    queryset = district_cases.objects.all()
    serializer_class = DistrictSerializer


@api_view(["GET"])
def EachStateView(request, s_name):
    queryset = district_cases.objects.all().filter(state_name=s_name)
    serializer = DistrictSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def EachCityCaseView(request, s_name, c_name):
    queryset = district_cases.objects.filter(state_name=s_name, city_name=c_name)
    serializer = DistrictSerializer(queryset, many=True)
    return Response(serializer.data)


date_ = str(dt.now()).split()[0]
# ignoring ssl error
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# function for opening url
def open_url(url_):
    try:
        res = requests.get(url_)
        js = res.json()
        return js

    except:
        fh = urllib.request.urlopen(url_, context=ctx)
        # .read() reads whole as a string
        data = fh.read().decode()
        js = json.loads(data)
        return js


confirmed__sum_before = states_cases.objects.all().aggregate(Sum("confirmed"))[
    "confirmed__sum"
]
Active__sum_before = states_cases.objects.all().aggregate(Sum("Active"))["Active__sum"]
Recovered__sum_before = states_cases.objects.all().aggregate(Sum("Recovered"))[
    "Recovered__sum"
]
Death__sum_before = states_cases.objects.all().aggregate(Sum("Death"))["Death__sum"]
date_before = str(states_cases.objects.values("Dated")[0]["Dated"])


def update_state():
    url_daily = "https://api.rootnet.in/covid19-in/stats/latest"
    js = open_url(url_daily)
    for i in js["data"]["regional"]:
        state_name_ = i["loc"]
        confirmed_ = i["totalConfirmed"]
        deaths_ = i["deaths"]
        recovered_ = i["discharged"]
        active_ = confirmed_ - (deaths_ + recovered_)

        # updating models
        changes = states_cases.objects.filter(state_name=state_name_)
        if confirmed_ > changes[0].confirmed:
            # print("Updating.... model state_cases =", state_name_)
            do_it = states_cases.objects.filter(state_name=state_name_).update(
                state_name=state_name_,
                confirmed=confirmed_,
                Death=deaths_,
                Recovered=recovered_,
                Active=active_,
                Dated=date_,
            )
        states_cases.objects.filter(state_name=state_name_).update(
            Dated=date_,
        )


# Cases Increment
def cases_increment():
    # total cases after _updating
    confirmed__sum_after = states_cases.objects.all().aggregate(Sum("confirmed"))[
        "confirmed__sum"
    ]
    Active__sum_after = states_cases.objects.all().aggregate(Sum("Active"))[
        "Active__sum"
    ]
    Recovered__sum_after = states_cases.objects.all().aggregate(Sum("Recovered"))[
        "Recovered__sum"
    ]
    Death__sum_after = states_cases.objects.all().aggregate(Sum("Death"))["Death__sum"]

    date_after = str(states_cases.objects.values("Dated")[0]["Dated"])
    print(f"DATE AFTER = {date_after}")

    inc = {
        "totalcases_inc": confirmed__sum_after - confirmed__sum_before,
        "day_before": date_before,
        "present_date": date_after,
        "death_inc": Death__sum_after - Death__sum_before,
        "recovered_inc": Recovered__sum_after - Recovered__sum_before,
    }

    query1 = CasesIncrementCheck.objects.all().first()
    confirmed_inc_ = query1.confirmed_inc
    present_date_ = query1.present_date
    death_inc = query1.death_inc
    recovered_inc = query1.recovered_inc
    day_before_ = query1.date_before
    doit = CasesIncrementCheck.objects.filter(present_date=present_date_).update(
        confirmed_inc=inc["totalcases_inc"],
        date_before=inc["day_before"],
        present_date=inc["present_date"],
        death_inc=inc["death_inc"],
        recovered_inc=inc["recovered_inc"],
        Dated=date_after,
    )
    print(f"DATA UPDATED in CasesIncrementCheck")


def update_district():
    url_district = "https://api.covid19india.org/state_district_wise.json"
    js1 = open_url(url_district)
    for state in js1:
        state_name_ = state
        for cities in js1[state_name_]["districtData"]:
            city_name_ = cities
            confirmed_ = js1[state_name_]["districtData"][city_name_]["confirmed"]
            recovered_ = js1[state_name_]["districtData"][city_name_]["recovered"]
            active_ = js1[state_name_]["districtData"][city_name_]["active"]
            deaths_ = js1[state_name_]["districtData"][city_name_]["deceased"]

            if city_name_ != f"Unknown":
                try:
                    changes = district_cases.objects.filter(city_name=city_name_)
                    if confirmed_ > changes[0].confirmed:
                        # print(
                        #     "Updating model district_cases =", state_name_, "->", city_name_
                        # )
                        do_it = district_cases.objects.filter(
                            city_name=city_name_
                        ).update(
                            state_name=state_name_,
                            city_name=city_name_,
                            confirmed=confirmed_,
                            Death=deaths_,
                            Recovered=recovered_,
                            Active=active_,
                        )
                        # do_it.save()
                    district_cases.objects.filter(city_name=city_name_).update(
                        Dated=date_,
                    )
                except:
                    pass

            elif city_name_ == f"Unknown":
                city_name_ = f"{city_name_}+{state_name_}"
                try:
                    changes = district_cases.objects.filter(city_name=city_name_)
                except:
                    changes = district_cases.objects.filter(
                        city_name=f"Unknown+{state_name_}"
                    )
                if confirmed_ > changes[0].confirmed:
                    # print(
                    #     "Updating model district_cases =", state_name_, "->", city_name_
                    # )

                    do_it = district_cases.objects.filter(city_name=city_name_).update(
                        state_name=state_name_,
                        city_name=city_name_,
                        confirmed=confirmed_,
                        Death=deaths_,
                        Recovered=recovered_,
                        Active=active_,
                    )
                district_cases.objects.filter(city_name=city_name_).update(
                    Dated=date_,
                )


##################################################################################
# Views
# rendering home page
def covid_state(request):
    date_1 = str(dt.now()).split()[0]  # todays date
    print("DATE1", date_1)
    dated1 = str(district_cases.objects.all().first().Dated)
    query_inc_before = CasesIncrementCheck.objects.all().first()
    dated2 = str(query_inc_before.Dated)
    dated3 = str(states_cases.objects.all().first().Dated)
    print("district_cases_dated1", dated1)
    print("CasesIncrementCheck dated2", dated2)
    print("states_cases dated3", dated3)

    if dated3 != date_1:
        print("UPDATE STATE")
        update_state()
        time.sleep(1)
        if dated2 != date_1:
            print("UPDATE cases inc")
            cases_increment()
    else:
        print("UP TO DATE")

    query_inc_after_updation = CasesIncrementCheck.objects.first()
    confirmed_inc_ = query_inc_after_updation.confirmed_inc
    present_date_ = query_inc_after_updation.present_date
    death_inc_ = query_inc_after_updation.death_inc
    recovered_inc_ = query_inc_after_updation.recovered_inc

    print(f"present _date{present_date_}")
    # sum either after updation or not , above if condition satisfies or not
    confirmed__sum = states_cases.objects.all().aggregate(Sum("confirmed"))
    Active__sum = states_cases.objects.all().aggregate(Sum("Active"))
    Recovered__sum = states_cases.objects.all().aggregate(Sum("Recovered"))
    Death__sum = states_cases.objects.all().aggregate(Sum("Death"))

    context_ = {
        "confirmed": confirmed__sum["confirmed__sum"],
        "Active": Active__sum["Active__sum"],
        "Death": Death__sum["Death__sum"],
        "Recovered": Recovered__sum["Recovered__sum"],
        "district_cases": district_cases.objects.all(),
        "states_cases": states_cases.objects.all().order_by("id"),
        "cases_increment": confirmed_inc_,
        "recovered_inc": recovered_inc_,
        "death_inc": death_inc_,
        "present_date": present_date_,
        "title": "INDIA",
        "state": "active",
    }
    return render(request, "covidtracker/home.html", context_)


# rendering district page
def covid_district(request):
    dated1 = str(district_cases.objects.values("Dated")[0]["Dated"])
    if dated1 != date_:
        update_district()
        print(f"UPDATING DISTRICT CASES on date= {date_}")
    else:
        print("DATA UP TO DATE")
    context_ = {
        "district_cases": district_cases.objects.all().order_by("id"),
        "title": "District",
        "district": "active",
    }
    return render(request, "covidtracker/district.html", context_)


def each_state(request, s_name):
    try:
        # question = Question.objects.get(pk=question_id)
        state_query = states_cases.objects.get(state_name=s_name)
        state_total_cases = states_cases.objects.get(state_name=s_name)
        state_data = district_cases.objects.filter(state_name=state_query)
        city_title = state_total_cases.state_name
    except state_query.DoesNotExist:
        raise Http404("State_query does not exist")

    context_ = {
        "title": city_title,
        "city": "active",
        "state_query": state_query,
        "state_data": state_data,
        "state_total_cases": state_total_cases,
    }
    return render(request, "covidtracker/city.html", context_)
