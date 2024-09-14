import tkinter as tk
from tkinter import font
import requests
import time

def getweather(event=None):
    city = textfield.get()
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=88b4dc688f4d1d018ee09c2c302f85ca"
    try:
        json_data = requests.get(api).json()
        if json_data['cod'] != 200:
            final_info = "City not found"
            final_data = ""
        else:
            condition = json_data['weather'][0]['main']
            temp = int(json_data['main']['temp'] - 273.15)
            min_temp = int(json_data['main']['temp_min'] - 273.15)
            max_temp = int(json_data['main']['temp_max'] - 273.15)
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']
            sunrise = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunrise'] - 21600))
            sunset = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunset'] - 21600))

            final_info = f"{condition}\n{temp}°C"
            final_data = (f"Max Temp: {max_temp}°C\n"
                          f"Min Temp: {min_temp}°C\n"
                          f"Pressure: {pressure} hPa\n"
                          f"Humidity: {humidity}%\n"
                          f"Wind Speed: {wind} m/s\n"
                          f"Sunrise: {sunrise}\n"
                          f"Sunset: {sunset}")

        label1.config(text=final_info)
        label2.config(text=final_data)
    except Exception as e:
        label1.config(text="Error")
        label2.config(text=str(e))


root = tk.Tk()
root.geometry("600x500")
root.title("Weather App")


f = ("poppins", 15, "bold")
t = ("poppins", 30, "bold")

textfield = tk.Entry(root, font=t)
textfield.pack(padx=20, pady=20)
textfield.focus()
textfield.bind('<Return>', getweather)

label1 = tk.Label(root, font=t)
label1.pack()
label2 = tk.Label(root, font=f)
label2.pack()


root.mainloop()
