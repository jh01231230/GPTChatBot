# Speech to text
import speech_recognition as sr
import os

if os.name == 'nt':
    import pyttsx3
else:
    from gtts import gTTS

class SpeechTextConvert(object):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def capture_voice_and_convert_to_text(self, timeout=3):
        MIN_ENERGY_THRESHOLD = 30
        MAX_ENERGY_THRESHOLD = 50
        use_ambient_noise_compensation = False # Otherwise use dynamic energy threshold adjustment
        
        while True:
            try:
                # Use the microphone as source of input
                with sr.Microphone() as source:
                    if use_ambient_noise_compensation:
                        # Prepare recognizer to recieve text
                        self.recognizer.adjust_for_ambient_noise(source, duration = 1.0)
                        print("Energy threshold: ", self.recognizer.energy_threshold)
                        if self.recognizer.energy_threshold < MIN_ENERGY_THRESHOLD:
                            self.recognizer.energy_threshold = MIN_ENERGY_THRESHOLD + self.recognizer.energy_threshold
                        if self.recognizer.energy_threshold > MAX_ENERGY_THRESHOLD:
                            self.recognizer.energy_threshold = MAX_ENERGY_THRESHOLD
                        print("Adjusted Energy threshold: ", self.recognizer.energy_threshold)
                    else:
                        self.recognizer.energy_threshold = (MIN_ENERGY_THRESHOLD + MAX_ENERGY_THRESHOLD) / 2
                        self.recognizer.dynamic_energy_threshold = True
                        self.recognizer.dynamic_energy_adjustment_damping = 0.15
                        self.recognizer.dynamic_energy_ratio = 1.5
                        print("Energy threshold: ", self.recognizer.energy_threshold)
                    
                    # Listens for the user's input
                    print("Ready to listen.")
                    audio = self.recognizer.listen(source, timeout=timeout)
                    
                    # Using Google to recognize audio
                    print("Sound captured.")
                    text = self.recognizer.recognize_google(audio)
                    
                return text
            except sr.RequestError as e:
                print("Could not request results: {0}".format(e))
            except sr.WaitTimeoutError as e:
                print("Timeout error occurred. No speech detected.")
            except Exception as e:
                print("An error occurred: ", str(e) if str(e) else "No input.")
                return ""
                
    def text_to_speech(self, text):
        if os.name == 'nt':  # 'nt' stands for Windows
            # Use pyttsx3
            engine = pyttsx3.init()
            #voices = engine.getProperty("voices")
            #engine.setProperty("voice", voices[0].id)
            engine.setProperty("rate", 150)
            engine.say(text)
            engine.runAndWait()
        else:
            # Use gTTS
            tts = gTTS(text=text, lang='en')
            # Save the converted audio to a file
            tts.save("output.mp3")
            # Play the audio file with mplayer
            os.system("mplayer output.mp3")
                
if __name__ == "__main__":
    stc_agent = SpeechTextConvert()
    text = stc_agent.capture_voice_and_convert_to_text()
    print(text)
    stc_agent.text_to_speech(text)
