import random

class Chatbot:
    def __init__(self):
        self.responses = {
            "hello": ["Hi there!", "Hello!", "Greetings!"],
            "how are you": ["I'm just a bot, but thanks for asking!", "I'm functioning well, thank you!", "I'm here and ready to chat!"],
            "bye": ["Goodbye!", "See you later!", "Take care!"],
            "tell me a joke": ["Why don't scientists trust atoms? Because they make up everything!", "What do you call a fake noodle? An impasta!", "Why did the scarecrow win an award? Because he was outstanding in his field!"],
            "default": ["I'm not sure what you mean.", "Could you please rephrase that?", "I'm here to chat, but I didn't quite understand that."]
        }

    def respond(self, user_input):
        user_input = user_input.lower()
        if user_input in self.responses:
            return random.choice(self.responses[user_input])
        else:
            return random.choice(self.responses["default"])

def main():
    chatbot = Chatbot()
    print("Chatbot: Hi! I'm a simple chatbot. You can talk to me about various topics.")
    while True:
        user_input =
