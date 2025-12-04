
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
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Logging configuration
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Initialize voice engine
engine = pyttsx3.init("sapi5")
engine.setProperty('rate', 170)
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

# Speak function
def speak(text):
    for sentence in text.split(". "):
        engine.say(sentence)
        engine.runAndWait()
    time.sleep(0.5)

# Take voice command function
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.5
        r.energy_threshold = 400
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("No speech detected. Try again.")
            return "none"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception as e:
        logging.info(e)
        print("Say that again please")
        return "none"

# Fetch Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found! Add it to your .env file.")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Gemini AI response
def gemini_model_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = (
            "You are JARVIS, a helpful voice assistant. "
            "Answer the user query clearly and concisely in maximum 50 words. "
            f"User query: {user_input}"
        )
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        else:
            return "Sorry, I couldn't generate a response."
    except Exception as e:
        logging.info(f"Gemini API error: {e}")
        return "Sorry, I could not get a response from Gemini."

# Greeting function
def greeting():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning Sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")
    speak("I am Jarvis. Please tell me how may I help you today?")

# Play random music function
def play_music():
    music_dir = "F:\\Data Science\\project\\JARVIS-voice-assistant-system_by_faria\\music"
    try:
        songs = os.listdir(music_dir)
        if songs:
            random_song = random.choice(songs)
            os.startfile(os.path.join(music_dir, random_song))
    except Exception as e:
        logging.info(f"Music play error: {e}")
        print("Error playing music.")

# Start assistant
greeting()

while True:
    query = takeCommand()
    if query == "none":
        continue

    # Exit commands
    if any(word in query for word in ["exit", "stop", "quit"]):
        speak("Shutting down. Goodbye!")
        logging.info("User exited the program.")
        break

    # Predefined commands
    elif "your name" in query:
        speak("My name is Jarvis")
    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {strTime}")
    elif "how are you" in query:
        speak("I am functioning in full capacity sir!")
    elif "who made you" in query:
        speak("I was created by Faria Sir!")
    elif "thank you" in query:
        speak("It's my pleasure sir. Always happy to help.")
    elif "open google" in query:
        speak("Opening Google, sir. Please type what you want to search.")
        webbrowser.open("https://www.google.com")
    elif "open github" in query:
        speak("Opening GitHub...")
        webbrowser.open("https://github.com")
    elif "open facebook" in query:
        speak("Opening Facebook...")
        webbrowser.open("https://www.facebook.com")
    elif "open youtube" in query:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com/")
    elif "open calculator" in query:
        speak("Opening calculator...")
        subprocess.Popen("calc.exe")
    elif "open notepad" in query:
        speak("Opening Notepad...")
        subprocess.Popen("notepad.exe")
    elif "open command prompt" in query or "command prompt" in query:
        speak("Opening Command Prompt...")
        subprocess.Popen("cmd.exe")
    elif "open calendar" in query or "calendar" in query:
        speak("Opening Google Calendar...")
        webbrowser.open("https://calendar.google.com/calendar/u/0/r")
    elif "joke" in query:
        jokes = [
            "Why did the computer get cold? Because it forgot to close its Windows.",
            "Why don’t robots ever get scared? Because they have steel nerves.",
            "Why was the math book sad? Because it had too many problems.",
            "Why don’t scientists trust atoms? Because they make up everything."
        ]
        speak(random.choice(jokes))
    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            speak(results)
        except Exception as e:
            logging.info(f"Wikipedia search error: {e}")
            speak("Sorry, I could not find any results.")
    elif "play music" in query or "music" in query:
        play_music()

    # All other queries go to Gemini AI
    else:
        response = gemini_model_response(query)
        if response:  # Only speak if Gemini returned something
            speak(response)
