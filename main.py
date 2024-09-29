import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

def get_weather(city):
    API_key = "f1b1a350c175b90b2ff01672c12b8dc3"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    try:
        res = requests.get(url)
        res.raise_for_status()  # Will raise an exception for 4xx/5xx responses
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Unable to retrieve data: {str(e)}")
        return None
    
    # Parse the response Json to get weather information
    weather = res.json()
    
    # Check if 'weather' key exists in the response
    if 'weather' not in weather or 'main' not in weather or 'sys' not in weather:
        messagebox.showerror("Error", "Incomplete data received from the API.")
        return None

    try:
        icon_id = weather['weather'][0]['icon']
        temperature = weather['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        description = weather['weather'][0]['description']
        city = weather['name']
        country = weather['sys']['country']
    except KeyError as e:
        messagebox.showerror("Error", f"Missing data: {str(e)}")
        return None

    # Get the icon URL and return all the weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)

def search():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "City name cannot be empty!")
        return

    result = get_weather(city)
    if result is None:
        return  # If there's an error, exit

    # If the city is found, unpack the weather information
    icon_url, temperature, description, city, country = result

    location_label.configure(text=f"{city}, {country}")

    try:
        image = Image.open(requests.get(icon_url, stream=True).raw)
        icon = ImageTk.PhotoImage(image)
        icon_label.configure(image=icon)
        icon_label.image = icon  # Keep reference to the image
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load weather icon: {str(e)}")
        return

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")

# Tkinter Window Setup
root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("400x400")

# City Entry
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

# Search Button
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# Labels for displaying weather information
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

icon_label = tk.Label(root)
icon_label.pack()

temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

description_label = tk.Label(root, font="Helvetica, 20")  # Added description_label
description_label.pack()

# Start the Tkinter event loop
root.mainloop()
