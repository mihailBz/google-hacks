import os

import google.generativeai as genai

import vertexai
from vertexai.preview import reasoning_engines

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI

from typing import List, Union, Dict

class GeminiCore:
    def __init__(self):
        
        self.project_id = "neon-opus-429019-j1"
        self.location = "us-central1"
        self.staging_bucket = "gs://creativity-1"

        vertexai.init(
            project=self.project_id, 
            location=self.location, 
            staging_bucket=self.staging_bucket
        )

        # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # self.model = genai.GenerativeModel("gemini-1.5-flash")
        # self.chat = self.model.start_chat(history=[])

    def _set_up(self) -> None:
        system = (
            "You are a helpful assistant that answers questions "
            "about Google Cloud."
        )

        human = "{text}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )
        chat = ChatVertexAI(project=self.project_id, location=self.location)
        self.chain = prompt | chat

    def send_message(self, question: str) -> Union[str, List[Union[str, Dict]]]:
        """Query the application.

        Args:
            question: The user prompt.

        Returns:
            str: The LLM response.
        """
        self._set_up()
        return self.chain.invoke({"text": question}).content
    
    # def send_message(self, message):
    #     return self.chat.send_message(message).text

    # def read_calendar(self, creds):
    #     return read_calendar_events(creds)
    #
    # def write_calendar(self, creds, event):
    #     return add_calendar_event(creds, event)
