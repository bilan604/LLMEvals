import time
import json
import datetime
from parsing import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


PATH = r'C:/Users/Bill/github/LLMEvals/geckodriver.exe'


# A template
class WebHelper(object):
    def __init__(self):
        self.driver = self.get_geckodriver()
        self.cached_items = []
        self.info = {}
        self.params = {}
        self.objects = {}
        self.functions = {
            "get": self.get,
            "write": self.write,
            "select": self.select,
            "click": self.click,
            "scroll": self.scroll,
            'cache': self.cache,  # store for one action
            'cache_xpath': self.cache_xpath,
            "obtain": self.obtain,  # default obtain by src
            "view_params": self.view_params
        }

    def debug_mode(self):
        errors = 0
        actions = []
        parse_splitter = "++++"
        for i in range(30):
            action = input("Debug Action:")
            print(f"{action=}\n")
            params = input("Debug Params:")
            print(f"{params=}\n")
            try:
                if parse_splitter in params:
                    params = params.split(parse_splitter)
                print(f"{params=}\n")
                
                instr = {
                    "instruction": action,
                    "params": params
                }

                print(f"{instr=}\n")

                self.handle_instruction(instr)

                actions.append(instr)
            except Exception as e:
                print("+++++++++++++++++++++++++++++++++++")
                print("Error:", e)
                errors += 1

    def get_geckodriver(self, headless=False):
        from selenium.webdriver.firefox.options import Options

        if not headless:
            driver = webdriver.Firefox(
                executable_path=PATH
            )
            return driver
        else:
            options = Options()
            options.headless = True

            driver = webdriver.Firefox(
                options=options,
                executable_path=PATH
            )
            return driver

    def instruct(self, instruction: str, params):
        print("\n--------------------->new instruction:")
        print(f"{instruction=}\n")
        print(f"{params=}\n")

        # replace param with specified param
        if type(params) == str:
            if params in self.params:
                params = self.params[params]
                print(f"{params=}\n")
        
        # passing in strings is depreciated
        if type(params) == str:
            params = [params]
        
        if len(params) == 1 and params[0] == "":
            resp = self.functions[instruction]()
        if len(params) == 1:
            resp = self.functions[instruction](params[0])
        if len(params) == 2:
            resp = self.functions[instruction](params[0], params[1])
        elif len(params) == 3:
            resp = self.functions[instruction](params[0], params[1], params[2])
        elif len(params) == 4:
            resp = self.functions[instruction](params[0], params[1], params[2], params[3])
        elif len(params) == 5:
            resp = self.functions[instruction](params[0], params[1], params[2], params[3], params[4])
        elif len(params) == 6:
            resp = self.functions[instruction](params[0], params[1], params[2], params[3], params[4], params[5])
        elif len(params) == 7:
            resp = self.functions[instruction](params[0], params[1], params[2], params[3], params[4], params[5], params[6])
        elif len(params) == 8:
            resp = self.functions[instruction](params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7])
        
        return resp

    def handle_instruction(self, instruction_object:dict):
        """
        access a cached item by specifying the name it was cached with
        """
        instruction = instruction_object["instruction"]
        print(f"{instruction=}\n")
        params = instruction_object["params"]
        print(f"{params=}\n")
        self.instruct(instruction, params)

    def handle_instructions(self, instructions):
        for instruction in instructions:
            self.handle_instruction(instruction)

    def view_params(self):
        for p, v in self.params.items():
            print("parameter name:", p)
            print("parameter value:", v)

    def get_xpath(self, element_type, label_rule, properties_rule):
        if label_rule == None:
            label_rule = lambda x: True
        if properties_rule == None:
            properties_rule = lambda x: True
        element = get_element(self.driver.page_source, element_type, label_rule, properties_rule)
        xpath = get_xpath_by_element(element)
        return xpath
    
    def generate_label_rule(self, param):
        lst = param.split(":")  #contains:these are some words
        if lst[0] == "contains":
            return lambda x: lst[1] in x
        if lst[0] == "equals":
            return lambda x: x.strip() == lst[1]
        if lst[0] == "containsLower":
            return lambda x: x.strip() == lst[1]
        return lambda x: True

    def generate_properties_rule(self, param):
        lst = param.split("||||")  #class||name_of_class||||text||the text
        
        # Maybe
        # class contains thistext and placeholder equals that
        def recu(idx, lst):
            if idx >= len(lst):
                return True
            element_type, value = lst[idx].split("||")
            ############ ONLY CONTAINS is possible rn
            return lambda x: element_type in x and value in x[element_type] and recu(idx+1, lst)

        return recu(0, lst)

    def cache(self, name:str, element_type: str, rule_specifier: str, rule_params: str):
        # name: name to store it as in self.params

        # rule_specifier: 'label' or 'properties'
        # rule_params: like 'contains:thistext' or 'class||thisTextInside'
        
        ## THIS CODE ALLOWS FOR ANY ELEMENT TO BE CATCHED BY SPECIFYING A RULE
        rule_maker_mapper = {
            "label": self.generate_label_rule,
            "properties": self.generate_properties_rule
        }
        rule_function = rule_maker_mapper[rule_specifier]
        rule = rule_function(rule_params)


        ## HERE IT IS BEING USED ON DEFAULT FOR XPATH
        xpath = None
        if rule_specifier == "label":
            xpath = get_element(element_type, rule, lambda x: True)
        elif rule_specifier == "properties":
            xpath = get_element(element_type, lambda x: True, rule)

        self.params[name] = xpath
        print("cached name:", name)
        print("cached xpath:", xpath)
        return

    
    def cache_xpath(self, name:str, element_type: str, rule_specifier: str, rule_params: str):
        # name: name to store it as in self.params
        # rule_specifier: 'label' or 'properties'
        # rule_params: like 'contains:thistext' or 'class||thisTextInside'
        
        ## THIS CODE ALLOWS FOR ANY ELEMENT TO BE CATCHED BY SPECIFYING A RULE
        rule_maker_mapper = {
            "label": self.generate_label_rule,
            "properties": self.generate_properties_rule
        }
        rule_function = rule_maker_mapper[rule_specifier]
        rule = rule_function(rule_params)

        ## HERE IT IS BEING USED ON DEFAULT FOR XPATH
        element = None
        if rule_specifier == "label":
            element = self.get_xpath(element_type, rule, lambda x: True)
        elif rule_specifier == "properties":
            element = self.get_xpath(element_type, lambda x: True, rule)

        self.params[name] = element
        print("cached:", name)
        return

    def obtain(self, func):
        # given a function, stores the xpath for later use
        xpath = func(self.driver.current_url, self.driver.page_source)
        self.params["xpath"] = xpath
        return xpath

    def get(self, url):
        self.driver.get(url)
        time.sleep(8)
    
    def select(self, XPATH, index):
        # could convert to waited
        select_element = self.driver.find_element(By.XPATH, XPATH)
        if not select_element:
            return False
        select_element = Select(select_element)
        select_element.select_by_index(index)
        return True

    def write(self, XPATH, keys):
        """
        Write can both take a cached xpath and also take an xpath 
        params is overriden by self.params[params]
        """
        if XPATH in self.params:
            XPATH = self.params[XPATH]
        # could convert to waited
        input_box = self.get_waited_element_by_xpath(XPATH)
        if not input_box:
            return False
        input_box.send_keys(keys)
        return True

    def click(self, XPATH):
        """
        Returns whether the click attempt was successful
        """
        # could convert to waited

        object = self.driver.find_element(By.XPATH, XPATH)
        # check whether the object is clickable (2 conditions must be satisfied)
        if object.is_displayed() and object.is_enabled():
            # this can still cause a crash, as some elements are obscured or hidden
            # i.e. a label is clickable, but can be obscured by a sometimes clickable
            # label associated with the label.
            object.click()
        else:
            print("Element is not clickable")

        time.sleep(1)
        return True
    
    def scroll(self):
        """
        This loads the page
        """
        time.sleep(3)
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, Math.round(document.body.scrollHeight));")
            time.sleep(2)
        time.sleep(3)
    
    def get_waited_element_by_xpath(self, xpath, limit=6):
        """
        gets an element waiting at most limit seconds
        """
        start_time = datetime.datetime.now()
        element = None
        curr_time = datetime.datetime.now()
        while not element and int((curr_time - start_time).total_seconds()) < limit:
            element = self.driver.find_element(By.XPATH, xpath)
            if element:
                return element
            time.sleep(1)
            curr_time = datetime.datetime.now()
        return None



class PoeHelper(WebHelper):
    def __init__(self):
        super().__init__()
        
        self.url = "https://poe.com/"
        self.selected_model = ""
        
        self.get("https://poe.com/login?redirect_url=%2F")

    def login(self):
        self.write('//input[@class="EmailInput_emailInput__4v_bn" and @type="email" and @placeholder="Email address" and @autocomplete="email"]', "bilan604gm@gmail.com")
        self.click('//button[@class="Button_buttonBase__0QP_m Button_primary__pIDjn" and text()="Go"]')

        code = input("Enter Code:")
        self.write('//input[@class="VerificationCodeInput_verificationCodeInput__YD3KV" and @placeholder="Code"]', code)
        self.click(self.get_xpath("button", lambda x: "log in" in x.lower(), None))
        time.sleep(3)

    def get_xpath(self, element_type, label_rule, properties_rule):
        if label_rule == None:
            label_rule = lambda x: True
        if properties_rule == None:
            properties_rule = lambda x: True
        element = get_element(self.driver.page_source, element_type, label_rule, properties_rule)
        xpath = get_xpath_by_element(element)
        return xpath
    