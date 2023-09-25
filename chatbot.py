from chatgpt import *
from stc import *
import datetime
import time
import random

class ChatBot(object):
    # Key words
    __bot_name = "Jarvis"
    __call_of_service = ["hi", "hey", "hello"]
    __cancel_the_service = ["nothing", "never mind"]
    
    # Preset sentences
    __greetings = ["Hello I am " + __bot_name + ". How can I help you?",
                   "Hello I am " + __bot_name + ". How may I help you?",
                   "Hello I am " + __bot_name + ". I am glad to help!",
                   "Good morning Sir/Madam. I am " + __bot_name + ". How can I help you?"]
    __service_cancelled = ["OK!"]
    __invalid_input = ["I don't understand. Please say it again."]
    
    def __init__(self):
        self.CNT_DOWN_TIME = 30
        self.end_time = datetime.datetime.now()
        
        self.gpt = ChatGPT() # GPT
        self.stc_agent = SpeechTextConvert() # Speech and text conversions
        
    def random_pick(self, a_list, func=lambda x: x):
        element = random.choice(a_list)
        element = func(element)
        return element
        
    def string_contains_any(self, input_string, list_of_strings):
        # Check if any string in the list is found in the input_string
        for s in list_of_strings:
            if s.lower() in input_string.lower():
                return True
        return False
        
    def string_is_any(self, input_string, list_of_strings):
        # Check if any string in the list is found in the input_string
        for s in list_of_strings:
            if s.lower() == input_string.lower():
                return True
        return False
        
    def greetings(self):
        def change_word(greeting):
            # Adjust based on time
            hour = int(datetime.datetime.now().hour)
            if hour > 12 and hour < 18:
                greeting = greeting.replace("morning", "afternoon")
            elif hour > 18 and hour < 24:
                greeting = greeting.replace("morning", "evening")
            return greeting
            
        # Random pick from greeting phrases
        greeting = self.random_pick(self.__greetings, change_word)
        
        # Output greetings
        self.stc_agent.text_to_speech(greeting)
    
    def wakeup(self):
        # If woke up
        if not self.check_sleep_status():
            return True
            
        # If not woke up, check the wake-up phrase
        print("Please say the wakeup phrase: 'Hi " + self.__bot_name + "'.")
        text = self.stc_agent.capture_voice_and_convert_to_text(1)
        if text and self.string_contains_any(text, self.__call_of_service) and self.__bot_name.lower() in text.lower():
            print("Waking up AI assistant...")
            self.greetings()
            self.to_sleep_timer(self.CNT_DOWN_TIME)
            return True
        return False

    def to_sleep_timer(self, seconds):
        # Get the current time
        now = datetime.datetime.now()
        # Calculate the end time
        self.end_time = now + datetime.timedelta(seconds=seconds)
            
    def check_sleep_status(self):
        # Get the current time
        now = datetime.datetime.now()
        if now >= self.end_time:
            return True
        return False
        
    def run(self):
        while True:
            if self.wakeup():
                # Convert speech through microphone to text
                text = self.stc_agent.capture_voice_and_convert_to_text()
                print("Input received: ", text)
                
                # Check if the input is any of the denail of service flag
                if text and self.string_is_any(text, self.__cancel_the_service):
                    self.stc_agent.text_to_speech(self.random_pick(self.__service_cancelled))
                    # Set to sleep
                    self.to_sleep_timer(0)
                    continue
                
                # Check if the user input makes sense
                print("Received voice, doing sense check.")
                if not text:
                    continue
                if self.gpt.sense_check(text):
                    print("Sense check passed, sending request to GPT.")
                    
                    # Send inquries to GPT engine and get the reply
                    response = self.gpt.process_inquiry(text)
                    print("Response received: ", response)
                    
                    # Convert replied text to synthetic speech 
                    print("Received the response, converting the response to voice.")
                    self.stc_agent.text_to_speech(response)
                    
                    # Reset sleep timer
                    self.to_sleep_timer(self.CNT_DOWN_TIME)
                else:
                    self.stc_agent.text_to_speech(self.random_pick(self.__invalid_input))
            
            # Pause for a second
            time.sleep(1)

def main():
    bot = ChatBot() # ChatBot
    bot.run()

if __name__ == "__main__":
    main()
