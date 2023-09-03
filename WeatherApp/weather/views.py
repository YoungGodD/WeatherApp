import requests
from django.shortcuts import render
import datetime

def index(request):
    API_KEY = 'your api_key'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + API_KEY

    if(request.method == 'POST'):
        city = request.POST.get('City')
    else:
        city = 'Moscow'

    res = requests.get(url.format(city)).json()

    try:
        tz = datetime.timezone(datetime.timedelta(seconds=int(res['timezone'])))
        date = datetime.datetime.now(tz=tz).strftime("%m-%d-%Y")
        time = datetime.datetime.now(tz=tz).strftime("%H:%M")
    except:
        return render(request, 'weather/error.html')

    city_info = {
        'city': city,
        'weather': res['weather'][0]['main'],
        'wind': res['wind']['speed'],
        'date': date,
        'time': time,
        'temp': round(res['main']['temp']),
        'temp_min': round(res['main']['temp_min']),
        'temp_max': round(res['main']['temp_max']),
        'icon': res['weather'][0]['icon']
    }

    context = {'info': city_info}

    return render(request, 'weather/index.html', context)


