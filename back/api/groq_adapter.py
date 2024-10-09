from constants import GROQ_API_KEY
from groq import Groq


class GroqAdapter():
    '''Class created to interact with Groq's API.'''
    def __init__(self):
        '''
        Initializes an instance with the API key stored in .env
        and sets up a client with this key.
        '''
        self.api_key = GROQ_API_KEY
        self.client = Groq(
            api_key=self.api_key
        )

    
    def get_response(self, message):
        '''
        Calls one of the AI models available in Groq to retrieve an answer
        for the message sent in the browser.
        '''
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
