import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib
import pyautogui
import pyjokes
import psutil

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
# there are two voices one of male(David) and one of female(Zira)
# david has id 0 and zira has id 1
# so here we set the voice of zira for our assistant
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # sender email and password
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 16:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am alexa. Please tell me how may I help you")


def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        # pause_threshold=seconds of non-speaking audio before a phrase is considered complete
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e) this prints the error that occured
        print("Say that again please...")
        return "None"
    return query


if __name__ == "__main__":
    wishMe()
    while True:
        # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            # sentences 2 means it will return 2 sentences from wikipedia
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'joke' in query:
            speak("I am sure you will find it funny")
            speak(pyjokes.get_joke())

        elif 'play music' in query:

            music_dir = 'E:\\Music'
            songs = os.listdir(music_dir)
            print(songs)
            # song[0] means it will start first song
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'screenshot' in query:
            pyautogui.screenshot('d:\\screenshot.png')

        elif "open word" in query:
            # respond("Opening Microsoft Word")
            os.startfile('Mention location of Word in your system')

        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "yourEmail@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'translate text' in query:
            try:
                speak("What should I translate?")
                MyText = takeCommand()
                MyText = MyText.lower()

                print("You Said : "+MyText)
                speak("Done")
                exit()
                # SpeakText(MyText)

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("unknown error occured")

        elif 'battery' or "power" in query:
            battery = psutil.sensors_battery()
            percent = str(battery.percent)

            speak("Your Device has"+percent+"percent of power left ")
            print("Your Device has"+percent+" % of power left")

        elif 'quit' in query:
            exit()
