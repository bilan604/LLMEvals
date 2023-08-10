
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


# A template
class WebHelper(object):
    def __init__(self):
        self.driver = self.get_geckodriver()
        self.info = {}
        self.params = {}
        self.objects = {}
        self.functions = {
            "get": self.get,
            "write": self.write,
            "select": self.select,
            "click": self.click,
            "scroll": self.scroll,
            "obtain": self.obtain  # default obtain by src
        }

    def get_geckodriver(self, headless=False):
        from selenium.webdriver.firefox.options import Options

        if not headless:
            driver = webdriver.Firefox(
                executable_path=r'C:/Users/Bill/projects/llm-evals/geckodriver.exe'
            )
            return driver
        else:
            options = Options()
            options.headless = True

            driver = webdriver.Firefox(
                options=options,
                executable_path=r'C:/Users/Bill/projects/llm-evals/geckodriver.exe'
            )
            return driver

    def handle_instruction(self, instruction_object):
        instruction = instruction_object["instruction"]
        params = instruction_object["params"]
        if params == "self":
            ##
            params = self.params["xpath"]

        resp = "Default empty response"
        if type(params) == str:
            resp = self.functions[instruction](params)
        elif type(params) in (list, tuple):
            if len(params) == 2:
                resp = self.functions[instruction](params[0], params[1])
            elif len(params) == 3:
                resp = self.functions[instruction](params[0], params[1], params[2])
        else:
            # functions
            resp = self.functions[instruction](params)

        return resp
    
    def handle_instructions(self, instructions):
        for instruction in instructions:
            self.handle_instruction(instruction)

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


