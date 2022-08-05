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
import time



class Test:
    def __init__(self, holder):
        self.holder = holder
        print("boutta get the driver")
        # self.driver = self.getDriver()
        # print("the system detected is: " + str(yeet))
        # self.monkeypox()

    def myFunction(self):
        print(self.holder)

    # def getDriver(self):

    #     options = webdriver.ChromeOptions()
    #     options._binary_location = "/usr/bin/chromium-browser"

    #     driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver",options=options)

    #     # options.add_argument('--profile-directory=Profile 8')
    #     # driver = webdriver.Chrome(path, options=options)
    #     return driver

    # def monkeypox(self):
    #         self.driver.get("https://vax4nyc.nyc.gov/patient/s/vaccination-schedule?page=Monkeypox")
    #         time.sleep(5)

    #         dateinput = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[3]/div/div/c-vcms-schedule-flow/main/div[2]/section[1]/div/section/c-vcm-screening-questions-section-a/div[1]/div[2]/div[2]/lightning-input[1]/lightning-datepicker/div/div/input")
    #         time.sleep(2)

    #         dateinput.send_keys("12/16/1995")

    #         zipcode = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[3]/div/div/c-vcms-schedule-flow/main/div[2]/section[1]/div/section/c-vcm-screening-questions-section-a/div[1]/div[2]/div[2]/lightning-input[2]/div/input")
    #         time.sleep(2)

    #         zipcode.send_keys("10016")

    #         time.sleep(2)
            
    #         radiobutton = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[3]/div/div/c-vcms-schedule-flow/main/div[2]/section[1]/div/section/c-vcm-screening-questions-section-a/div[1]/div[2]/div[3]/div/lightning-radio-group/fieldset/div/span[2]/label/span[1]")
    #         time.sleep(2)

    #         radiobutton.click()

    #         nextbutton = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[3]/div/div/c-vcms-schedule-flow/main/div[2]/section[2]/div[1]/div/button[2]")
    #         time.sleep(2)

    #         nextbutton.click()

    #         time.sleep(6)

    #         notavailable = self.driver.find_elements(By.XPATH, "/html/body/div[5]/div/div[3]/div/div/c-vcms-schedule-flow/main/div[2]/section[1]/div/section/c-vcms-book-appointment/article")

    #         appointments_available = False
    #         response = False

    #         for elem in notavailable:
    #             try:
    #                 text = elem.text
    #                 text = text.lower()
    #                 if "no appointments are currently available" in text:
    #                     appointments_available = False
    #                     print("No appointments are currently available.")
    #                 else:
    #                     print("Appointments may be available; something changed.")
    #                     appointments_available = True
    #             except:
    #                 continue
    #             if appointments_available:
    #                 return "YES"
    #             else:
    #                 return "NO"

    #         return "something else"






if __name__ == '__main__':
    x = "hi"
    bot = Test(x)
