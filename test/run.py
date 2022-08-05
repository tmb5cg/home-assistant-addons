# import os
# import os.path
# import platform
# import time
# from datetime import date, datetime
# from decimal import Decimal
# from os import path
# from time import sleep
# from tokenize import Double
# from venv import create

# import paho.mqtt.client as mqtt
# import undetected_chromedriver as uc
# from selenium import webdriver
# from selenium.common.exceptions import (NoSuchElementException,
#                                         TimeoutException, WebDriverException)
# from selenium.webdriver import Chrome, ChromeOptions
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support import ui
# from selenium.webdriver.support.wait import WebDriverWait


import platform



class Test:
    def __init__(self, holder):
        self.holder = holder
        system = platform.system()
        print("the system detected is: " + str(system))

    def myFunction(self):
        print(self.holder)




if __name__ == '__main__':
    x = "hi"
    bot = Test(x)
    bot.myFunction()
