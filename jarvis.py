import speech_recognition as sr
import pyttsx3
import logging
import os
import datetime
import wikipedia
import webbrowser
import random
import subprocess
import google.generativeai as genai

# logging configuration
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"   # removed extra space
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Activating voice from our system
engine = pyttsx3.init("sapi5")
engine.setProperty('rate', 170)
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)
print(voices[1].id)

# This is speak function
def speak(text):
    """
    This function converts text to voice
    Args:
       text
    Returns:
       voice
    """
    engine.say(text)
    engine.runAndWait()

# This function recognizes the speech and converts it to text
def takeCommand():
    """
    This function takes command and recognizes it
    
    Returns:
       text as query
    """
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")
    except Exception as e:
        logging.info(e)
        print("Say that again please")
        return "None"
    return query
def gemini_model_response(user_input):
    try:
        GEMINI_API_KEY = "AIzaSyCYVLZ5mmo7yQ7fv4-yZusnbYay119eaxM"
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"Answer the following question shortly and clearly:\n{user_input}"

        response = model.generate_content(prompt)

        if response and response.text:
            return response.text.strip()
        else:
            return "Sorry, I couldn't generate a response."

    except Exception as e:
        return f"Error: {str(e)}"

def greeting():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour<=12:
        speak("Good Morning Sir!")
    elif hour >=12 and hour<=18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")
    speak("I am Jarvis.Please tell me how may I help you today?")
def play_music():
    music_dir = "F:\\Data Science\\project\\JARVIS-voice-assistant-system_by_faria\\music"
    try:
       songs= os.listdir(music_dir)
       print(songs)
       if songs:
           random_song = random.choice(songs)
           os.startfile(os.path.join(music_dir,random_song))
    except Exception as e:
        print(e)
greeting()
while True:
    query = takeCommand().lower()
    print(query)
    
    if "your name" in query:
        speak("My name is Jarvis")
        logging.info("User asked for assistant's name.")
    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {strTime}")
    elif "exit" in query:
        speak("Thank you for your time,Sir.")
        logging.info("User exited the program.")
        exit()
    elif "how are you" in query:
        speak("I am functioning in full capacity sir!")
        logging.info("User asked about assistant's well-being.")
    elif "who made you" in query:
        speak("I was created by Faria Sir!")
        logging.info("User asked about assistant's creator.")
    elif "thank you" in query:
        speak("It's my pleasure sir. Always happy to help.")
        logging.info("User expressed gratitude.")
    elif "open google" in query:
        speak("ok sir. please type here what do you want to read")
        webbrowser.open("google.com")
        logging.info("User requested to open google.")
    elif "open github" in query:
        speak("opening github....")
        webbrowser.open("github.com")
        logging.info("User requested to open github.")
    elif "open facebook" in query:
        speak("opening facebook....")
        webbrowser.open("facebook.com")
        logging.info("User requested to open facebook.")
    elif 'open youtube' in query:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com/")
        logging.info("User requested to open youtube.")

    elif "open calculator" in query or "calculator" in query:
        speak("opening calculator")
        subprocess.Popen("calc.exe")
        logging.info("User requested to open calculator.")
    elif "open notepad" in query or "notepad" in query:
        speak("opening Notepad....")
        subprocess.Popen("Notepad.exe")
        logging.info("User requested to open notepad.")
    elif "open commad prompt" in query or "command prompt" in query:
        speak("opening commad prompt")
        subprocess.Popen("cmd.exe")
        logging.info("User requested to open command prompt.")
    elif "open calendar" in query or "calendar" in query:
        speak("opening calendar")
        webbrowser.open("https://calendar.google.com/calendar/u/0/r")
        logging.info("User requested to open calendar.")
    elif "joke" in query:
        jokes = [
        "Why did the computer get cold? Because it forgot to close its Windows.",
        "Why don’t robots ever get scared? Because they have steel nerves.",
        "Why was the math book sad? Because it had too many problems.",
        "Why don’t scientists trust atoms? Because they make up everything."
        ]
        joke = random.choice(jokes)
        speak(joke)
    elif "wikipedia" in query:
        speak("Searching wikipedia...")
        query=query.replace("wikipedia","")
        results = wikipedia.summary(query,sentences=2)
        speak("According to wikipedia")
        speak(results)
        logging.info("User requested information from wikipedia.")
    elif "play_music" in query or "music" in query:
        play_music()

    
    else:
        response = gemini_model_response(query)
        speak(response)
        logging.info("User asked for other questions")
