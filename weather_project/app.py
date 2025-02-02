import streamlit as st
import requests
from datetime import datetime

def get_weather_data(city, api_key):
    url = 'https://api.openweathermap.org/data/2.5/weather?' + 'appid=' + api_key + '&q=' + city
    response = requests.get(url)
    return response.json()

def weather_description(data):
    temperature = data['main']['temp'] - 273.15
    description = data['weather'][0]['description']
    return f"The weather in your city is {description} with a temperature of {temperature:.1f} degrees Celsius."

def get_weekly_forecast(weather_api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_api_key}" 
    response = requests.get(url)
    return response.json()

def display_weekly_forecast(data):
    st.write('')
    st.write('### Weekly Weather Forecast')
    displayed_dates = set()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric('', 'Day')
    with c2:
        st.metric('', 'Desc')
    with c3:
        st.metric('', 'Min_temp')
    with c4:
        st.metric('', 'Max_temp')
    
    for day in data['list']:
        date = datetime.fromtimestamp(day['dt']).strftime('%A, %B, %d')

        if date not in displayed_dates:
            displayed_dates.add(date)
            min_temp = day['main']['temp_min'] - 273.15
            max_temp = day['main']['temp_max'] - 273.15
            description = day['weather'][0]['description']

            with c1:
                st.write(f"{date}")
            with c2:
                st.write(f"{description.capitalize()}")
            with c3:
                st.write(f"{min_temp:.1f} degress Celcius")
            with c4:
                st.write(f"{max_temp:.1f} degress Celcius")


def main():
    st.sidebar.title('Weather Prediction Model')
    city = st.sidebar.text_input('Type the name of the city', 'San Francisco')
    enter = st.sidebar.button('Generate Weather')

    weather_api_key = 'enter weather api key here'

    if enter:
        st.title(city + ' Weather Updates')
        with st.spinner('Fetching weather data...'):
            weather_data = get_weather_data(city, weather_api_key)
            if weather_data.get('cod') != 404:
                col1, col2 = st.columns(2)
                with col1: 
                    st.metric('Temperature', f"{weather_data['main']['temp'] - 273.15:.2f} degress Celcius")
                    st.metric('Humidity', f"{weather_data['main']['humidity']}%")
                with col2:
                    st.metric('Pressure', f"{weather_data['main']['pressure']} hPa")
                    st.metric('Wind Speed', f"{weather_data['wind']['speed']} m/s")
                
                weather_descrip = weather_description(weather_data)
                st.write(weather_descrip)

                forecast_data = get_weekly_forecast(weather_api_key, weather_data['coord']['lat'], weather_data['coord']['lon'])

                if forecast_data.get('cod') != '404':
                    display_weekly_forecast(forecast_data)
                else:
                    st.error('Error Ocurred!!')


            else:
                st.error('Error Occured')

if __name__ == '__main__':
    main()
