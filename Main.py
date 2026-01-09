import speech_recognition as sr
import webbrowser 
import musiclib
from openai import OpenAI
from gtts import gTTS         
import pygame
import os
import time
is_speaking = False
active_ai = False
name = "RAHUL"
recognizer = sr.Recognizer()
# -----------------------------------Speak function---------------------------------------------------
def speak(text):
     global is_speaking
     is_speaking = True
     tts = gTTS(text = text,lang = 'en')
     tts.save('temp.mp3')
     pygame.mixer.init()
     pygame.mixer.music.load('temp.mp3')
     pygame.mixer.music.play()
     while pygame.mixer.music.get_busy():
        time.sleep(0.1)

     pygame.mixer.music.unload()
     os.remove("temp.mp3")
     is_speaking = False
# -----------------------------------AI CONTROL---------------------------------------------------
def aiprocess(comand):
    client = OpenAI(api_key = os.getenv("OPEN_API_KEY"))
    response = client.responses.create(
         model="gpt-5-nano",
        input=f"Answer briefly in 1 sentence only: {comand}"
        #  max_output_tokens=40   # 👈 limits output size/
)

    return(response.output_text)
# -----------------------------------BASICS COMMANDS--------------------------------------------------
def processComand(c):
    global ai_active
    if "activate ai" in c.lower():
          ai_active = True
          speak("Activating AI")
          speak("You are connect to Jarvis AI, How may i help you")
          return
    if "deactivate ai" in c.lower():
            ai_active = False
            speak("AI mode deactivated.")
            return
    # print(c)
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open instagram" in c.lower():
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")
    elif "open faceebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open github" in c.lower():
        speak("Opening Github")
        webbrowser.open("https://github.com/Raah2003")
    elif "open linkedin" in c.lower():
        speak("Opening Linkedin")
        webbrowser.open("https://www.linkedin.com/in/rahul-kushwah-136719309/")
    elif "open cv" in c.lower():
         speak("Opening cv")
         webbrowser.open("file:///C:/Users/Dell/OneDrive/Desktop/Rahul_python_developer2.pdf")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclib.music.get(song)
        if link:
           speak("Playing YOur Song")
           webbrowser.open(link)
        else:
            speak("Somg not found")
    else:
        if ai_active:  # if ai_active = true -----> AI ON
           output = aiprocess(c)
           print("AI:",output)
           speak(output)
        else:
            speak("Say Activate AI to talk with me")
# -------------------------Main program--------------------------------------------------------------------------------
if __name__ == "__main__":
    speak("hey I am AI Powered Virtual Assistance developed by Rahul The Pyhton Developer . Say Jarvis to Activate me")
    while True:
       if is_speaking:
          continue   #don't listen whille speak
       
       # Reading Microphone as source
       # listening the speech and store in audio_text variable
       # Recognize speech using Google Web Speech API
       try:
           with sr.Microphone() as source:
               recognizer.adjust_for_ambient_noise(source)
               print("Listening.............")
               audio_text = recognizer.listen(source, timeout =2, phrase_time_limit = 4)
           word = recognizer.recognize_google(audio_text).lower()
           print("Heard",word)
           if(word == "jarvis"):
               speak("Yes, How may i help you?")
               with sr.Microphone() as source:
                   print("Jarvis Active.............")
                   audio_text = recognizer.listen(source,timeout =3,  phrase_time_limit = 6)
                   comand = recognizer.recognize_google(audio_text)
                   processComand(comand)
                   print(comand)
           elif(word == "good bye"):
                  speak(f"good bye {name}")
                  print("okk byeee.........")
                  break
       except sr.UnknownValueError:
           print("error audio")
       except Exception as e:
            print(e,"Sorry, I did not get that")
