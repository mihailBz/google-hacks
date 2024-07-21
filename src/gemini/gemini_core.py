import os

import google.generativeai as genai


class GeminiCore:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message):
        return self.chat.send_message(message).text

    # def read_calendar(self, creds):
    #     return read_calendar_events(creds)
    #
    # def write_calendar(self, creds, event):
    #     return add_calendar_event(creds, event)
