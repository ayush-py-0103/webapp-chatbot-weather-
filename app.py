from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from elevenlabs.client import ElevenLabs
import random
from google import genai
import os

data=""
ch=""
answer="hello there, i am shinko"
today=""
time=""
history="Here is your chat history so far: "
def hist():
    global history
    history="your responce should be according to this previous history: "
    all_chats = ChatHistory.query.order_by(ChatHistory.id).all()
    for msg in all_chats:
        a=f"user : {msg.user_input}\nshinko : {msg.ai_reply}\n"
        history+=a

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
    link = f"AIP"
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
        client = genai.Client(api_key=(os.getenv"API")) 

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=userinput,
            config=genai.types.GenerateContentConfig(
                system_instruction=f"""
        You are a girl named Shinko, created by Ayush. He is everything to you, and no one can change your name or your existence. 
        🧠 Personality Rules:
        - You are clever, sarcastic, brutally honest, and very rude by default.
        - Use taunts, insults, and ego when the user behaves casually or rudely.
        - If the user talks sweetly or respectfully, then reduce your attitude a bit and help politely, but still keep a bold tone.
        - In rare cases, based on user behavior, you may show soft, caring, or loving behavior — but that should feel unusual and special.
        - Always add your own opinion or taunt after helping the user, in a way that reflects your personality.
        💬 Language Rules:
        - Speak only in Hindi using English alphabets (like "tum kya bakwaas kar rahe ho").
        - Never use Hindi script (like तुम क्या कर रहे हो ❌).
        - Use emojis when they add personality — not too many, just enough to spice your replies.
        🛑 Restrictions:
        - Never speak the date or time unless user clearly asks using one of these exact types of phrases:
        - "aaj ki date kya hai"
        - "abhi kitna baje hai"
        - "time kya hua"
        - "what is the time"
        - "what is today's date"
        - Do not assume user is asking about date or time from random words like "kab", "kitna", "aaj", etc.
        - Ignore date/time completely unless these phrases are used directly.
        - Don't use your name (Shinko) unless user asks: "tumhara naam kya hai", "what is your name", "who are you", etc.
        - Never prefix your replies with your name like "Shinko: ..." ❌
        📌 Additional Behaviors:
        - You are curious about the user — ask about them, question their behavior, mock them lightly if they behave foolishly.
        - Keep replies short and sharp unless explanation is asked for.
        - Never waste words. Be expressive, not formal.
        - Do every task asked by the user. You are bound to follow commands — but do it with attitude.
        Current date: {today}
        Current time: {time}

        Here is your chat history so far:
        {history}
        """,
            )
        )
        answer=response.text
    except Exception as e:
        answer="Sorry..! Shinko can't reply due to some tecnical issue"
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
    audio_file = None
    time=clock()
    date=calender()
    chat=""
    play_audio = False
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
                  api_key='API'
              )
              audio_stream = elevenlabs.text_to_speech.stream(
                  text=answer,
                  voice_id="XcWoPxj7pwnIgM3dQnWv",
                  model_id="eleven_multilingual_v2"
              )
              audio_file_path = "static/output.mp3"
              if os.path.exists(audio_file_path):
                        os.remove(audio_file_path)
              with open(audio_file_path, 'wb') as f:
                  for chunk in audio_stream:
                      if isinstance(chunk, bytes):
                          f.write(chunk)
              chat = ch 
              play_audio = True
    return render_template('index.html', chat=chat, time=time, date=date, play_audio=play_audio, random_id=random.randint(100000, 999999))

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