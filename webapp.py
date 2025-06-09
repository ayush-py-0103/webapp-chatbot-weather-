from flask import Flask, render_template, request
import requests
from datetime import datetime



def clock():
    current = datetime.now()
    hr= int(current.strftime("%H"))
    min=current.strftime("%M")
    if hr>12:
        hr=hr-12
        min=min + " PM"
    else:
        min=min + " AM"
    return f"{hr}:{min}"

def calender():
    current = datetime.now()
    day= int(current.strftime("%d"))
    mon= int(current.strftime("%m"))
    year= int(current.strftime("%Y"))
    months=["january","february","march","april","may","june","july","august","september","october","november","december"]
    return f"{day}, {months[mon-1]}, {year}" 

def wthr(city):
    link = f"https://api.weatherapi.com/v1/current.json?key=52f08ebd7ef54de584e24528252303&q={city}"
    response = requests.get(link)
    data = response.json()
    if "error" in data:
        print("City not found.")
    else:
        location = data["location"]["name"]
        country = data["location"]["country"]
        weather = data["current"]["condition"]["text"]
        temperature = data["current"]["temp_c"]
        return f"The weather in {location}, {country} is {weather} with a temperature of {temperature}°C."

app =  Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        temp=wthr(city)
        time=clock()
        date=calender()
    return render_template('index.html', temp=temp, time=time, date=date)

@app.route("/abc")
def yalo():
    return render_template("index1.html")

if __name__ == '__main__':
    app.run(debug=True)
