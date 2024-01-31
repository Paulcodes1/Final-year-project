from import_modules import *

class SpeechTranslatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Speech-to-Text and Translation")

        self.translator = Translator()
        self.translated_speech = []
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.text_output = tk.Text(master, height=10, width=50)
        self.text_output.pack()

        self.start_button = tk.Button(master, text="Start Listening", command=self.start_listening)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Listening", command=self.stop_listening)
        self.stop_button.pack()

        self.save_button = tk.Button(master, text="Save Translations", command=self.save_translations)
        self.save_button.pack()

        self.is_listening = False

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.speech_thread = threading.Thread(target=self.listen_and_translate)
            self.speech_thread.daemon = True
            self.speech_thread.start()

    def stop_listening(self):
        self.is_listening = False

    def listen_and_translate(self):
        with self.microphone as source:
            while self.is_listening:
                print("Listening...")
                try:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)  # Adapt to ambient noise
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio, language='en-US')
                    translated_text = self.translator.translate(text, dest='en').text  # Translate to English
                    self.translated_speech.append(translated_text)  # Store translated speech
                    print("Translated Text:", translated_text)
                    self.update_text_output("\n".join(self.translated_speech))  # Update GUI with all translated speech
                except sr.UnknownValueError:
                    print("Could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Error occurred: {e}")

    def update_text_output(self, text):
        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(tk.END, text)

    def save_translations(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt"),
                                                              ("Word files", "*.docx"),
                                                              ("PDF files", "*.pdf"),
                                                              ("All files", "*.*")])
        if file_path:
            #Determine  the file format based on the chosen file extension
            file_format = file_path.split(".")[-1]
            with open(file_path, 'w', encoding='utf-8') as file:
                if file_format == "txt":
                    file.write("\n".join(self.translated_speech))
                elif file_format =="docx":
                    self.save_as_docx(file_path)
                elif file_format =="pdf":
                    self.save_as_pdf(file_path)

    def save_as_docx(self, file_path):
        document = Document()
        for translation in self.translated_speech:
            document.add_paragraph(translation)
        document.save(file_path) 

    def save_as_pdf(self, file_path):
        c = canvas.Canvas(file_path)
        for translation in self.translated_speech:
            c.drawString(100, 100, translation)
            c.showPage()
        c.save()           


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechTranslatorApp(root)
    root.mainloop()
