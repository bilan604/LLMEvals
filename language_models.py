import re
import openai
from webhelper import *


class Prompter(object):
    def __init__(self):
        self.description = "Contains functions for multiple LLMs"
        self.webhelper = None  # WebHelper()
        self.model_map = {
            "gpt-4": self.GPT_4,
            "bard": self.Google_Bard
        }

    def prompt(self, model, input):
        response = self.model_map[model](input)
        return response

    def parse_input(self, input):
        """
        Converts an OpenAI registry evaluation input to a generalized llm prompt
        In case theres more than just a system prompt
        """
        system_cont = ""
        user_cont = ""
        for pe in input:
            if pe["role"] == "system":
                system_cont = pe["content"]
            elif pe["role"] == "user":
                user_cont = pe["content"]
        
        prompt = \
        """\
{system_cont}

{user_cont}"""
        prompt = re.sub("{system_cont}", system_cont, prompt)
        prompt = re.sub("{user_cont}", user_cont, prompt)        
        return prompt

    def GPT_4(self, input):
        #input=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": query}]

        # hyperparameters are set literal
        response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=input,
                temperature=0.5,
                max_tokens=1200,
                frequency_penalty=0.0
            ).choices[0].message.content.strip()
        return response
    
    def Google_Bard(self, input):
        # ToDo: Implement
        print("INPUT", input)
        # need to have firefox open by the time this is called
        prompt = self.parse_input(input)
        response = self.bard_chat.query(prompt)
        return response
















