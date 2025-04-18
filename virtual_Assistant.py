import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import webbrowser


recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()


voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[0].id)  
tts_engine.setProperty('rate', 150)  

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """Listen for user input via microphone and convert to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Network error. Please try again.")
            return ""

def greet_user():
    """Greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning! How can I help you today?")
    elif 12 <= hour < 18:
        speak("Good afternoon! What can I do for you?")
    else:
        speak("Good evening! How may I assist you?")

def open_website(query):
    """Open a website based on the query."""
    if 'youtube' in query:
        webbrowser.open('https://www.youtube.com')
        speak("Opening YouTube")
    elif 'google' in query:
        webbrowser.open('https://www.google.com')
        speak("Opening Google")
    elif 'facebook' in query:
        webbrowser.open('https://www.facebook.com')
        speak("Opening Facebook")
    elif 'twitter' in query:
        webbrowser.open('https://www.twitter.com')
        speak("Opening Twitter")
    else:
        speak("Sorry, I can't open that website.")

def play_song_on_youtube(song_name):
    """Play a song on YouTube using pywhatkit."""
    speak(f"Playing {song_name} on YouTube.")
    pywhatkit.playonyt(song_name)

def tell_time():
    """Tell the current time."""
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    speak(f"The time is {current_time}")

def fetch_wikipedia_info(query):
    """Fetch information from Wikipedia."""
    query = query.replace('who is', '').strip()
    speak(f"Searching Wikipedia for {query}.")
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"There are multiple results for {query}. Can you be more specific?")
    except wikipedia.exceptions.PageError:
        speak(f"Sorry, I couldn't find any information on {query}.")

def handle_command(query):
    """Handle different voice commands."""
    if 'time' in query:
        tell_time()
    elif 'open' in query:
        open_website(query)
    elif 'play' in query:
        song_name = query.replace('play', '').strip()
        if song_name:
            play_song_on_youtube(song_name)
        else:
            speak("Please specify the name of the song.")
    elif 'who is' in query or 'what is' in query:
        fetch_wikipedia_info(query)
    elif 'exit' in query or 'bye' in query:
        speak("Goodbye! Have a nice day.")
        exit()
    else:
        speak("I'm not sure how to help with that. Can you try something else?")

def main():
    """Main function to run the virtual assistant."""
    greet_user()
    while True:
        query = listen()
        if query:
            handle_command(query)

if __name__ == "__main__":
    main()
