import re
import openai
from load import *
from webhelper import *
import pyautogui as pag


class Prompter(object):
    def __init__(self):
        self.description = "Contains functions for multiple LLMs"
        self.webhelper = None  # WebHelper()
        self.screen_width = -1
        self.screen_height = -1
        screen_width, screen_height = pag.size()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.objects = {}

        # gpt-3.5?
        self.poe_models = [ 
            "GPT-4",
            "Claude-2-100k",
            "Claude-instant",
            "GPT-4-32k",
            "Google-PaLM",
            "Llama-2-70b",
            "Llama-2-13b",
            "Llama-2-7b"
        ]
        self.model_map = {
            "gpt-4": self.GPT_4,
            "bard": self.Google_Bard
        }

        self.gpt_models = ["gpt-4", "gpt-3.5-turbo-16k"]

        # used to store alternate responses from bard
        self.cache = {}
        

    def prompt(self, model, input):
        if model not in self.gpt_models:
            prompt = self.parse_input(input)
        else:
            # the input is in the default openai api call format
            prompt = input

        response = None
        if model in self.poe_models:
            ###########################
            ###########################
            # CloudFlare
            if not self.webhelper:
                self.webhelper = PoeHelper()
                self.webhelper.login()
            
            # checks should be built into the functions
            # this function can be redeclared as a dependency if necessary
            select_model(self.webhelper, model)
            send_message(self, prompt, model)
            response = get_response(self)

        else:
            response = self.model_map[model](prompt)

        return [prompt, response]

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
    
    def Google_Bard(self, prompt):
        # ToDo: Implement
        resp = self.objects['bard'].get_answer(prompt)
        
        # store the alternate responses
        if "choices" in resp:
            self.cache[resp["response_id"]] = resp["choices"]

        response = resp["content"]
        print("Bard response:", response)
        print("----------------")
        return response

def select_model(webhelper, model):
    expected_url = "https://poe.com/" + model
    if webhelper.driver.current_url != expected_url:
        webhelper.get(expected_url)
    time.sleep(2)


def get_response(prompter):
    # Note: div, class=Message_humanMessageBubble__Nld4j for sent messages
    messages = get_messages(prompter.webhelper.driver.page_source)
    
    if not messages:
        return None

    response = messages.pop()
    return response

def send_message(prompter, message, model_name="Assistant"):        
    text_area_xpath = '//textarea[@placeholder="Talk to {model_name} on Poe"]'
    text_area_xpath = re.sub("{model_name}", model_name, text_area_xpath)
    prompter.webhelper.handle_instruction({
        "instruction": "click",
        "params": text_area_xpath
    })
    prompter.webhelper.handle_instruction({
        "instruction": "write",
        "params": (text_area_xpath, message)
    })
    prompter.webhelper.handle_instruction({
        'instruction': 'click',
        'params': '//button[@class="Button_buttonBase__0QP_m Button_primary__pIDjn ChatMessageSendButton_sendButton__OMyK1 ChatMessageInputContainer_sendButton__s7XkP"]'
    })
    return

def get_messages(src):
    # This gets bot messages
    print(f"{len(src)=}")
    soup = BeautifulSoup(src, 'html.parser')
    divs = soup.find_all('div', {'class': 'Message_botMessageBubble__CPGMI Message_widerMessage__SmSLi'})
    divs = list(map(str, divs))
    divs = list(map(lambda div: re.sub("<(br|/br|p|/p)>", " ", div), divs))
    divs = list(map(lambda div: re.sub("</br>", " ", div), divs))
    divs = list(map(lambda div: re.sub("<.+?>", " ", div), divs))
    divs = list(map(lambda div: re.sub(" +", " ", div), divs))
    return divs


# screen_width, screen_height = pyautogui.size()


