"""
get_menu_context – для всех страниц
get_wind_direction – для главной страницы
index_page – для главной страницы
reviews – для страницы с отзывами
preloader – для страницы с прелоадером
"""
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from oop_django.forms import FeedbackForm
from oop_django.models import FeedbackHistory
from datetime import date
import requests


def get_wind_direction(degree):
    """
    Функция get_wind_direction передовит градусную меру направления ветра в слова
    :param degree: направление ветра в градусах
    :return: направление ветра
    """
    if degree >= 337 or degree <= 23:
        return 'North'
    elif 23 < degree < 67:
        return 'Northeast'
    elif 67 <= degree <= 112:
        return 'East'
    elif 112 < degree < 157:
        return 'Southeast'
    elif 157 <= degree <= 203:
        return 'South'
    elif 203 < degree < 247:
        return 'Southwest'
    elif 247 <= degree <= 292:
        return 'West'
    elif 292 < degree < 337:
        return 'Northwest'


def get_menu_context(request):
    """
    Функция get_menu_context возращает основное меню сайта
    :param request: запрос
    :return: основное меню сайта
    """
    menu = []

    menu.append({"link": "/", "text": "Main page"})
    menu.append({"link": "/reviews", "text": "Reviews"})

    if request.user.is_authenticated:
        menu.append({"link": "/logout", "text": "Logout"})
    else:
        menu.append({"link": "/login", "text": "Login"})

    return {'menu': menu}


@login_required()
def index_page(request):
    """
    Функция index_page заполняет данными основную страницу по запросу
    :param request: запрос
    """
    city = "Москва"

    if request.method == 'POST':
        city = request.POST.get('input_city')

    context = get_menu_context(request)

    context["user"] = request.user

    context["today"] = []

    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    city_id = 0
    appid = "27bf4a8b5bbee00be332c0488636cff1"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()

        context["city"] = city
        context["today"].append({"month": months[date.today().month]})
        context["today"].append({"date": date.today().day})
        context["today"].append({"temperature": data['list'][0]['main']['temp']})
        context["today"].append({"feels_like": data['list'][0]['main']['feels_like']})
        context["today"].append({"minimal_temperature_daily": data['list'][0]['main']['temp_min']})
        context["today"].append({"maximal_temperature_daily": data['list'][0]['main']['temp_max']})
        context["today"].append({"pressure": data['list'][0]['main']['pressure']})
        context["today"].append({"humidity": data['list'][0]['main']['humidity']})
        context["today"].append({"wind_speed": data['list'][0]['wind']['speed']})
        context["today"].append({"wind_direction": get_wind_direction(data['list'][0]['wind']['deg'])})
        context["today"].append({"weather": data['list'][0]['weather'][0]['description']})

    except Exception as e:
        print("Exception (find):", e)
        pass

    return render(request, "index.html", context)


def reviews(request):
    """
    Функция reviews заполняет страницу с ранее написанными отзывами
    :param request: запрос
    """
    context = get_menu_context(request)

    if request.method == "POST":
        form = FeedbackForm(request.POST)

        text = request.POST.get("review")

        if form.is_valid():
            item = FeedbackHistory(date=datetime.datetime.now, text=text)
            item.save()

            context["text"] = text
            context["form"] = form

        else:
            context['form'] = form

    else:
        context['nothing_entered'] = True
        context['form'] = FeedbackForm()

    items = FeedbackHistory.objects.all()

    context["items"] = items

    return render(request, "reviews.html", context)


def preloader(request):
    """
    Функция reviews заполняет страницу прелоадера
    :param request: запрос
    """
    context = {

    }

    return render(request, "preloader.html", context)
