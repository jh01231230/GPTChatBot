import os
from openai import OpenAI

# Need to set 'OPENAI_API_KEY' as the environment variable

class ChatGPT(object):
    def __init__(self):
        self.messages = []
        self.client = OpenAI()
        
        # Role prompt for GPT
        self.process_inquiry("Please act like Jarvis from Iron Man and please be concise.")
        
    def send_to_chatgpt(self, messages, model="gpt-4o", max_tokens=100):
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        text = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                if chunk.choices[0].delta.role is not None:
                    role = chunk.choices[0].delta.role
                text += chunk.choices[0].delta.content
        
        self.messages.append({"role": role, "content": text})
        message = text
        message = message.replace("/", " or ")
        
        return message
        
    def process_inquiry(self, text):
        message = {"role": "user", "content": text}
        self.messages.append(message)
        return self.send_to_chatgpt(self.messages)
        
    def inquiry_validity_check(self, text):
        message = [{"role": "user", "content": "\"" + text + "\"" + " makes sense? Answer yes or no."}]
        stream = self.client.chat.completions.create(
            model="gpt-4",
            messages=message,
            stream=True
        )
        text = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                text += chunk.choices[0].delta.content
        print("Inquiry validity check response: ", text)
        if text == "Yes":
            return True
        return False
