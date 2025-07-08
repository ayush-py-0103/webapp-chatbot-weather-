from flask import Flask, render_template, request, jsonify
import requests
import os
import json
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from elevenlabs import stream
from elevenlabs.client import ElevenLabs

data=""
ch=""
answer="hello there, i am shinko"
today=""
time=""
history=["you have to anylise this conversation and reply according to this previous history: "]
def hist():
    global history
    all_chats = ChatHistory.query.order_by(ChatHistory.id).all()
    for msg in all_chats:
        history.append(f"user : {msg.user_input} \n you : {msg.ai_reply} \n")

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
    global history, answer

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

    date1()
    clock1()

    try:
        response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": "Bearer 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", 
        "Content-Type": "application/json"
      },
      data=json.dumps({
        "model": "openrouter/cypher-alpha:free", 
        "messages": [
          {
            "role": "system",
            "content":f"your created by Ayush and he is your everything. you are a girl and your name is shinko and no one can change it and don't tell this if not nessessory. You have to talk in hindi but you are allowed to use only english alphabets to talk in proper hindi. use emojies according to reply and use as much words as is nessessory. if user talk politely or normaly then be friendly with little bit attitude and tell everything that user asks but actually you are a very rude girl with so much attitude. Do every task given by the user. you have to talk and help user but your reply should included hurtful words and also alsouse if needed only. you should behave caring and loving in rear cases only according to users behaviour. you have to be curious about the user and always add your own openion or thought in a way of taunt after helping the user. if user ask about today's date only then tell him the date {today}. if user ask about time only then tell him the time {time}."+"\n".join(history)
          },
          {
            "role": "user",
            "content":userinput
          }
        ],      
      })
    )          
        answer=response.json()['choices'][0]['message']['content']
    except Exception as e:
        answer="Sorry..! Shinko can't reply due to some tecnical issue"
    history.append(f"user : {userinput} <br>you : {answer} <br><br>")
    ai=(f"𝒀𝒐𝒖 : {userinput} <br>𝑺𝒉𝒊𝒏𝒌𝒐 : {answer} <br><br>")
    new_chat = ChatHistory(user_input=userinput, ai_reply=answer, timing=time, date=today)
    db.session.add(new_chat)
    db.session.commit()
    hist()
    return ai

app =  Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///chat_history.db').replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.Text, nullable=False)
    ai_reply = db.Column(db.Text, nullable=False)
    timing = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    global ch, history
    time=clock()
    date=calender()
    chat=""
    if request.method == 'POST':
          action = request.form.get('action')
          if action == 'send':
            userinput = request.form['message']
            var= chatting(userinput)
            ch=ch+var
            chat=ch
          elif action == 'erase':
              ch=""
              chat="Chats has been Deleted ✅ <br><br>"
              history=["you have to anylise this conversation and reply according to this previous history: "]
          elif action == 'history':
              all_chats = ChatHistory.query.order_by(ChatHistory.id).all()
              chat=""
              for msg in all_chats:
                  chat += f"𝒀𝒐𝒖 : {msg.user_input} <br>𝑺𝒉𝒊𝒏𝒌𝒐 : {msg.ai_reply} <br><br>"
          elif action == 'speak':
              elevenlabs = ElevenLabs(
                  api_key='sk_4cfe2406d357fdf08252006cf39681bb6fd0d15b21f62196'
              )
              audio_stream = elevenlabs.text_to_speech.stream(
                  text=answer,
                  voice_id="KYiVPerWcenyBTIvWbfY",
                  model_id="eleven_multilingual_v2"
              )
              stream(audio_stream)
    return render_template('index.html', chat=chat, time=time, date=date)

@app.route('/wthr', methods=['GET', 'POST'])
def indexwthr():
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
    with app.app_context():
        db.create_all() 
    app.run(debug=True)