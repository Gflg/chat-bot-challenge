from constants import GROQ_API_KEY
from groq import Groq


class GroqAdapter():
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.client = Groq(
            api_key=self.api_key
        )

    
    def get_response(self, message):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
