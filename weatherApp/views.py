from django.shortcuts import render
import requests
from datetime import datetime

# Create your views here.


def weather(request):
	url = "http://api.openweathermap.org/data/2.5/weather?q="
	api_key = 'paste your api key here'
	cityname = request.GET.get('city')
	
	try:

		if cityname is None:
			context = {
						'date':datetime.now,
						'celsius':'NA-/',
						'country':'NA-/',
						'celsius':'NA-/',
						'fahrenheit':'NA-/',
						'feel':'NA-/',
						'wind_speed':'NA-/',
						'weather':'NA-/',
						'pressure':'NA-/',
						'humidity':'NA-/',
						'visibility':'NA-/'}
			return render(request,'weather.html',context)
		else:
			response = requests.get(url+cityname+'&appid='+api_key).json()
			cel = response['main']['temp_max'] - 273.15
			fr = cel*9/5+32
			city = response['name']
			country = response['sys']['country']
			feel = response['main']['feels_like']
			wind_speed = response['wind']['speed']
			weather = response['weather'][0]['description']
			pressure = response['main']['pressure']
			humidity = response['main']['humidity']
			visibility = response['visibility']

			next_5_day_url = "http://api.openweathermap.org/data/2.5/forecast?q="
			next_5_day_url_response = requests.get(next_5_day_url+cityname+'&mode=json'+'&appid='+api_key).json()
			


			cel_5 = []
			fr_5 = []
			feel_5 = []
			wind_speed_5 = []
			weather_5 = []
			pressure_5 = []
			humidity_5 =[]
			visibility_5 = []
			date_5 = []


			for i in range(0,40):
				cel_5.append(next_5_day_url_response['list'][i:i+1][0]['main']['temp_max'] - 273.15)
				fr_5.append(cel_5[i]*9/5+32)
				wind_speed_5.append(next_5_day_url_response['list'][i:i+1][0]['wind']['speed'])
				weather_5.append(next_5_day_url_response['list'][i:i+1][0]['weather'][0]['main'])
				pressure_5.append(next_5_day_url_response['list'][i:i+1][0]['main']['pressure'])
				humidity_5.append(next_5_day_url_response['list'][i:i+1][0]['main']['humidity'])
				visibility_5.append(next_5_day_url_response['list'][i:i+1][0]['visibility'])
				date_5.append(next_5_day_url_response['list'][i:i+1][0]['dt_txt'])


			five_days_data =  list(zip(cel_5,fr_5,wind_speed_5,weather_5,pressure_5,humidity_5,visibility_5,date_5))

			context = {'date':datetime.now,
						'celsius':cel,
						'fahrenheit':fr,
						'city':city,
						'country':country,
						'feel':feel,
						'wind_speed':wind_speed,
						'weather':weather,
						'pressure':pressure,
						'humidity':humidity,
						'visibility':visibility,
						'five_days_data':five_days_data,
						}
			return render(request,'weather.html',context)

	except:
		return render(request,'error.html')
