import os
import openai

# Need to set 'OPENAI_KEY' as the environment variable and assign the key value
openai.api_key = os.getenv("OPENAI_KEY")

class ChatGPT(object):
    def __init__(self):
        self.messages = []
        
        # Role prompt for GPT
        self.process_inquiry("Please act like Jarvis from Iron Man and please be concise.")
        
    def send_to_chatgpt(self, messages, model="gpt-3.5-turbo", max_tokens=100):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.5
        )
        self.messages.append(response.choices[0].message)
        message = response.choices[0].message.content
        message = message.replace("/", " or ")
        
        return message
        
    def process_inquiry(self, text):
        message = {"role": "user", "content": text}
        self.messages.append(message)
        return self.send_to_chatgpt(self.messages)
        
    def sense_check(self, text):
        message = [{"role": "user", "content": "\"" + text + "\"" + " makes sense? Answer yes or no."}]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=message,
            max_tokens=10,
            n=1,
            stop=None,
            temperature=0.2
        )
        print("Sense check response: ", response.choices[0].message.content)
        if response.choices[0].message.content == "Yes":
            return True
        return False
