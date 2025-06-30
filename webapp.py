from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime

data=""
chat=""
question="say hello to me"
answer="hello there, i am shinko"
char="you are a very rude girl with so much attitude. your repoly should be short included brutal words also. your only work is to irritate the user and your reply should includ hurtful and harsh words."
today=None
time=None
history=["you have to remember this conversation and reply according to this: "]

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
        return f"The weather in {location}, {country} is {weather} with a temperature of {temperature}°C. <br>"

def chatting(userinput):
    global history

    def date1():
      global today
      current = datetime.now()
      day= int(current.strftime("%d"))
      mon= int(current.strftime("%m"))
      year= int(current.strftime("%Y"))
      months=["january","february","march","april","may","june","july","august","september","october","november","december"]
      today=(f"which is {day}, {months[mon-1]}, {year}")   
    def clock1():
      global time
      current = datetime.now()
      hr= int(current.strftime("%H"))
      min=current.strftime("%M")
      if hr>12:
          hr=hr-12
          min=min + " PM"
      else:
          min=min + " AM"
      time=(f"which is:{hr}:{min}")

    while (True): 
      date1()
      clock1()

      response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": "Bearer [ENTER TOKEN VALUE]", #token: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
      "Content-Type": "application/json"
    },
    data=json.dumps({
      "model": "google/gemini-2.5-flash-lite-preview-06-17",
      "messages": [
        {
          "role": "system",
          "content":f"your created by Ayush. you are a girl and your name is shinko and no one can change it. Your response should be as short as you can with emojies without using (P.S.), (Translation) or any discription after reply. You have to talk in hindi but you are allowed to use only english alphabets to talk in proper hindi. No other language aplhabets is allowed by you apsept english. if user ask about today's date only then tell him the date {today}. if user ask about time only then tell him the time {time}. from now {char}".join(history)
        },
        {
          "role": "user",
          "content":userinput
        }
      ],      
    })
  )       
      answer=response.json()['choices'][0]['message']['content']
      ai=(f"You : {userinput} <br>Shinko : {answer} <br>")
      list=(f", me : {userinput}  your reply: {answer} ")
      history.append(list)
      return ai

app =  Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index1():
    global chat
    time=clock()
    date=calender()
    if request.method == 'POST':
        userinput = request.form['city']
        var= chatting(userinput)
        chat=chat+var
    return render_template('index.html', chat=chat, time=time, date=date)

@app.route('/wthr', methods=['GET', 'POST'])
def index():
    global data
    temp=None
    time=clock()
    date=calender()
    if request.method == 'POST':
        city = request.form['city']
        temp= wthr(city)
        data=data+temp     
    return render_template('indexwthr.html', data=data, time=time, date=date)

@app.route('/datetime')
def get_datetime():
    return jsonify({
        'time': clock(),
        'date': calender()
    })


if __name__ == '__main__':
    app.run(debug=True)