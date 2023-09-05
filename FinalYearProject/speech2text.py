import speech_recognition as sr
import threading
import tkinter as tk
from googletrans import Translator

#Initialize variables
translator = Translator()
translated_speech = []

#Function to start and handle speech recognition
def start_listening():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        while True:
            print("Listening...")
            try:
                recognizer.adjust_for_ambient_noise(source, duration=1) #Adapt to ambient noise
                audio = recognizer.listen(source, phrase_time_limit=5)
                text = recognizer.recognize_google(audio, language='en-US') #English - United States
                translated_text = translator.translate(text, dest='en').text #Translate to English
                translated_speech.append(translated_text) #Store translated speech
                print("Translated Text: ", translated_text)
                update_text_output("\n".join(translated_speech)) #Update GUI with all translated speech
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError as e:
                print(f"Error occurred: {e}")

#Function to update text output on the GUI
def update_text_output(text):
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, text)

#Create the main window
root = tk.Tk()
root.title("Speech-to-Text Converter")

text_output = tk.Text(root, height=10, width=50)
text_output.pack()

#Start the speech recognition thread
speech_thread = threading.Thread(target=start_listening)
speech_thread.daemon = True
speech_thread.start()

root.mainloop()