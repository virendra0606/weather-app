from django.shortcuts import render
import json
import urllib.request
from django.contrib import messages
from datetime import datetime

# Create your views here.
def index(request):
    data={}
    if request.method=='POST':
        cityname=request.POST.get('city')
        if cityname!="":
            try:
                res=urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+cityname+'&appid=d9ae5542b18578e87d4ba137e6ec7c6e').read()
                Json_data = json.loads(res)
                weather = Json_data['weather']

                def convert_date_time(time_stamp,time_zone):
                    local_time = datetime.utcfromtimestamp(time_stamp + time_zone)
                    return local_time.strftime("%I:%M:%S %p")
                
                sunrise = convert_date_time((Json_data['sys']['sunrise']),Json_data['timezone'])
                sunset = convert_date_time((Json_data['sys']['sunset']),Json_data['timezone'])
                
                current_time =datetime.now()
                current_date = current_time.date()
                current_Time = current_time.time()
                print(current_Time)

                data ={
                    'city':str(Json_data['name']),
                    'country_code':str(Json_data['sys']['country']),
                    'coordinate':str(Json_data['coord']['lon']) + '.' + str(Json_data['coord']['lat']),
                    'temprature':str(Json_data['main']['temp'] )+ "k",
                    'pressure':str(Json_data['main']['pressure']),
                    'weather':weather,
                    'current_date':current_date,
                    'current_Time':current_Time,
                    'humidity':str(Json_data['main']['humidity']),
                    'wind':str(Json_data['wind']['speed']),
                    'sunrise':sunrise,
                    'sunset':sunset,
                    'jsondata':Json_data,
                    'cityname':cityname,
                    'wind':str(Json_data['wind']['speed'])+'km/h', #+str(Json_data['wind']['deg'])+' '+str(Json_data['wind']['gust']),
                    }
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    messages.error(request, "City not found! Please enter a valid city name.")
                else:
                    messages.error(request, f"HTTP Error: {e.code}")
                
        
        else:
            messages.error(request,"................Enter City Name.................")
            return render(request,"weatherUi.html")
    return render(request,"weatherUi.html",data)

# def New(request):
#     return render(request,"weatherUi.html")
