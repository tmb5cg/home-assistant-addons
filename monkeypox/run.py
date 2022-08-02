import os
import os.path
import platform
import time
from datetime import date, datetime
from decimal import Decimal
from os import path
from time import sleep
from tokenize import Double
from venv import create

import paho.mqtt.client as mqtt
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui
from selenium.webdriver.support.wait import WebDriverWait


class InstaBot:
    def __init__(self, driver, queue):
        self.driver = driver
        self.queue = ""
        self.appointments_available = False


    def mainFunc(self):
        # self.startup_methods()
        print("Initializing...")
        response = self.monkeypox()
        
        # send response
        self.send_to_mqtt(response)


    def send_to_mqtt(self, response):
        print(f"Calling meter.last_read()..")
        if response.lower() == "NO":
            response = 0.5
        elif response.lower() == "YES":
            response = 2
        else:
            response=0

        startTime = response

        message = {'startTime': startTime}

        print(f"message: {message}")

        # mqtthost = os.getenv("MQTT_HOST")
        # mqttuser = os.getenv("MQTT_USER")
        # mqttpass = os.getenv("MQTT_PASS")

        mqtthost = '192.168.1.15'
        mqttuser = 'mosquitto'
        mqttpass = 'mosq'

        print(f"Connecting to mqtt {mqtthost} as {mqttuser}")

        mqttc = mqtt.Client("oru_meter_reader")
        mqttc.username_pw_set(username=mqttuser, password=mqttpass)
        mqttc.connect(mqtthost)

        print(f"Publishing to mqtt")

        print(f"Publishing electric_meter/startTime: {startTime}")
        mqttc.publish('monkeypox/startTime', startTime, retain=True)
        time.sleep(1)


        print(f"Disconnectig from mqtt")
        mqttc.disconnect()

        print(f"DONE\n\n")

    def monkeypox(self):
        self.driver.get("https://vax4nyc.nyc.gov/patient/s/vaccination-schedule?page=Monkeypox")
        time.sleep(5)

        dateinput = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[3]/div/div/c-vcms-schedule-flow/main/div[2]/section[1]/div/section/c-vcm-screening-questions-section-a/div[1]/div[2]/div[2]/lightning-input[1]/lightning-datepicker/div/div/input")
        time.sleep(2)

        dateinput.send_keys("12/16/1995")

        zipcode = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[3]/div/div/c-vcms-schedule-flow/main/div[2]/section[1]/div/section/c-vcm-screening-questions-section-a/div[1]/div[2]/div[2]/lightning-input[2]/div/input")
        time.sleep(2)

        zipcode.send_keys("10016")

        time.sleep(2)
        
        radiobutton = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[3]/div/div/c-vcms-schedule-flow/main/div[2]/section[1]/div/section/c-vcm-screening-questions-section-a/div[1]/div[2]/div[3]/div/lightning-radio-group/fieldset/div/span[2]/label/span[1]")
        time.sleep(2)

        radiobutton.click()

        nextbutton = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[3]/div/div/c-vcms-schedule-flow/main/div[2]/section[2]/div[1]/div/button[2]")
        time.sleep(2)

        nextbutton.click()

        time.sleep(6)

        notavailable = self.driver.find_elements(By.XPATH, "/html/body/div[5]/div/div[3]/div/div/c-vcms-schedule-flow/main/div[2]/section[1]/div/section/c-vcms-book-appointment/article")

        appointments_available = False
        response = False

        for elem in notavailable:
            try:
                text = elem.text
                text = text.lower()
                if "no appointments are currently available" in text:
                    appointments_available = False
                    print("No appointments are currently available.")
                else:
                    print("Appointments may be available; something changed.")
                    appointments_available = True
            except:
                continue
            if appointments_available:
                return "YES"
            else:
                return "NO"

        return "something else"

def create_driver():
    system = platform.system()
    if system == 'Darwin':
        path = 'chrome_mac/chromedriver'
    elif system == 'Linux':
        path = 'chrome_linux/chromedriver'
    elif system == 'Windows':
        path = os.getcwd() + '\chrome_windows\chromedriver.exe'

    use_undetected_chromedriver = True

    if use_undetected_chromedriver:
        options = uc.ChromeOptions()
        # options.add_argument('--profile-directory=Profile 8')
        options.headless = True
       
        driver = uc.Chrome(options=options)
        return driver

    else: 
        options = webdriver.ChromeOptions()
        options.add_argument('--profile-directory=Profile 8')
        driver = webdriver.Chrome(path, options=options)
        return driver


if __name__ == '__main__':
    driver = create_driver()
    bot = InstaBot(driver, "")
    bot.mainFunc()
