import os
import asyncio
import paho.mqtt.client as mqtt
import json
import logging
import time
import pyppeteer
import shutil
import requests

# start of class definitions here
class MeterError(Exception):
    pass


class Meter(object):
    MFA_TYPE_SECURITY_QUESTION = 'SECURITY_QUESTION'
    MFA_TYPE_TOTP = 'TOTP'
    SITE_CONED = 'coned'
    DATA_SITE_CONED = 'cned'
    SITE_ORU = 'oru'
    DATA_SITE_ORU = 'oru'

    def __init__(self, email, password, mfa_type, mfa_secret, account_uuid, meter_number, account_number=None, site='coned', loop=None, browser_path=None):
        self._LOGGER = logging.getLogger(__name__)

        """Return a meter object whose meter id is *meter_number*"""
        self.email = email
        if self.email is None:
            raise MeterError("Error initializing meter data - email is missing")
        # _LOGGER.debug("email = %s", self.email.replace(self.email[:10], '*'))

        self.password = password
        if self.password is None:
            raise MeterError("Error initializing meter data - password is missing")
        # _LOGGER.debug("password = %s", self.password.replace(self.password[:9], '*'))

        self.mfa_type = mfa_type
        if self.mfa_type is None:
            raise MeterError("Error initializing meter data - mfa_type is missing")
        self._LOGGER.debug("mfa_type = %s", self.mfa_type)
        if self.mfa_type not in [Meter.MFA_TYPE_SECURITY_QUESTION, Meter.MFA_TYPE_TOTP]:
            raise MeterError("Error initializing meter data - unsupported mfa_type %s", self.mfa_type)

        self.mfa_secret = mfa_secret
        if self.mfa_secret is None:
            raise MeterError("Error initializing meter data - mfa_secret is missing")
        # _LOGGER.debug("mfa_secret = %s", self.mfa_secret.replace(self.mfa_secret[:8], '*'))

        self.account_uuid = account_uuid
        if self.account_uuid is None:
            raise MeterError("Error initializing meter data - account_uuid is missing")
        # _LOGGER.debug("account_uuid = %s", self.account_uuid.replace(self.account_uuid[:20], '*'))

        self.meter_number = meter_number.lstrip("0")
        if self.meter_number is None:
            raise MeterError("Error initializing meter data - meter_number is missing")
        # _LOGGER.debug("meter_number = %s", self.meter_number.replace(self.meter_number[:5], '*'))

        self.account_number = account_number

        self.site = site
        if site == Meter.SITE_CONED:
            self.data_site = Meter.DATA_SITE_CONED
        elif site == Meter.SITE_ORU:
            self.data_site = Meter.DATA_SITE_ORU
        self._LOGGER.debug("site = %s", self.site)
        if self.site not in [Meter.SITE_CONED, Meter.SITE_ORU]:
            raise MeterError("Error initializing meter data - unsupported site %s", self.site)

        self.loop = loop
        self._LOGGER.debug("loop = %s", self.loop)

        self.browser_path = browser_path
        self._LOGGER.debug("browser_path = %s", self.browser_path)


    async def post_story(self):
        """Posts to instagram story"""
        try:
            await self.browse()

            return "success"
        except Exception as e:
            print(e)
            raise MeterError("Error posting to story")

    async def browse(self):
        # Define browser configuration
        browser_launch_config = {
        "defaultViewport": {"width": 390, "height": 844},
        "dumpio": True,
        "headless": False,
        "isMobile": True,
        "args": ["--no-sandbox", "--disable-software-rasterizer"]}
        if self.browser_path is not None:
            browser_launch_config['executablePath'] = self.browser_path

        # Create browser
        browser = await pyppeteer.launch(browser_launch_config)

        # Go to new tab, set user agent to iPhone to allow for file upload
        page = await browser.newPage()
        await page.setUserAgent("Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/100.0.4896.85 Mobile/15E148 Safari/604.1")

        # Go to instagram
        await page.goto('https://www.instagram.com', {'waitUntil' : 'domcontentloaded'})

        # Sleep so loading can finish
        time.sleep(10)

        # Click "I want to log in" to beat splash page
        try:
            # Get all buttons on page - elementHandles
            all_buttons = await fetch_elements(page, '[type="button"]')

            # Find button we want, and click it, then peel out
            for button in all_buttons:
                button_text = await page.evaluate('(el) => el.textContent', button)
                print(str(button_text))
                if str(button_text) == "Log In":
                    # await page.evaluate('window.alert("Found the button with this text, going to click next!!!!");')
                    time.sleep(4)
                    await button.click()
                    break
                
        except Exception as e:
            print("exception on 2nd is " + str(e))
            alerts = 'window.alert("' + str(e) + '");'
            await page.evaluate('window.alert("1st one no work!!!!");')
            # await page.evaluate(alerts)

        # Enter login
        try:
            # Enter email
            loginBox = await page.querySelector('[aria-label = "Phone number, username, or email"]')
            time.sleep(3)
            await loginBox.type("@gmail.com")

            # Enter password - SET THESE VALUES TO PRIVATE UPON GIT COMMIT
            time.sleep(2)
            passwordBox = await page.querySelector('[aria-label = "Password"]')
            await passwordBox.type("")

        except Exception as e:
            print("last exception was: " + str(e))


        # Finalize login
        try:
            
            # 1. Get all button of type="submit"
            # 2. For each of these button(s), check if they have a div whose text value is "Log In"
            # //*[@id="loginForm"]/div[1]/div[6]/button
            time.sleep(3)

            all_buttons = await fetch_elements(page, 'button > div')

            # Find button we want, and click it, then peel out
            for button in all_buttons:
                button_text = await page.evaluate('(el) => el.textContent', button)
                print(str(button_text))
                if str(button_text) == "Log In":
                    # await page.evaluate('window.alert("found final login button lets go");')
                    time.sleep(4)
                    await button.click()
                    break                
            time.sleep(5)
            # print("refreshing page to ignore the Not Now button")

            await page.goto('https://www.instagram.com', {'waitUntil' : 'domcontentloaded'})

            time.sleep(10)
            time.sleep(15)

            # await loginSubmitButton.click()


        except Exception as e:
            print("last exception was: " + str(e))

        time.sleep(5)
        print("LOGIN SUCCESFUL")




        # CLICK POST STORY
        try:
            time.sleep(3)
            all_buttons = await fetch_elements(page, 'button > span > div')

            # Find button we want, and click it, then peel out
            for button in all_buttons:
                button_text = await page.evaluate('(el) => el.textContent', button)
                print(str(button_text))
                if str(button_text) == "Your Story":
                    await page.evaluate('window.alert("FOUND STORY BUTTON!!!");')
                    time.sleep(4)
                    await button.click()
                    time.sleep(15)
                    break                
            time.sleep(5)
        except:
            print("last method broke")
            time.sleep(15)



    async def browse2(self):

        browser_launch_config = {
            "defaultViewport": {"width": 390, "height": 844},
            "dumpio": True,
            "headless": False,
            "args": ["--no-sandbox", "--disable-gpu", "--disable-software-rasterizer"]}
        if self.browser_path is not None:
            browser_launch_config['executablePath'] = self.browser_path

        # Create browser
        browser = await pyppeteer.launch(browser_launch_config)

        # Open new tab and go to reddit
        page = await browser.newPage()
        await page.goto('https://old.reddit.com/r/ProgrammerHumor/top/?sort=top&t=week', {'waitUntil' : 'domcontentloaded'})

        logging.info('opened reddit')
        print("opened reddit")

        # Store fetched images and memos here 2D arr
        memeUrlsAndDescriptions = []
        
        # Fetch and store all elements in list
        reddit_content = await fetch_elements(page, 'a.title.may-blank.outbound')
        if reddit_content is None:
            logging.error('Fetching reddit elements failed')
            return
        else:
            logging.info('Iterating over page 1 items')

            for e in reddit_content:
                title = await page.evaluate('(element) => element.textContent', e)
                url = await page.evaluate('(element) => element.getAttribute("data-href-url")', e)

                combined = [url, title]
                memeUrlsAndDescriptions.append(combined)
                print(title)
                print(str(url))

        # SAVE IMAGES USING REQUESTS -- ADD PROXY
        imgCounter = 0
        for i in memeUrlsAndDescriptions:
            url = i[0]
            response = requests.get(url, stream=True)

            img_save_path = '/Users/tucker/Documents/GitHub/home-assistant-addons/dcsm/imgs/'
            filename = 'img_' + str(imgCounter) + '.png'
            filepath = img_save_path + filename
            imgCounter += 1
            with open(filepath, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            time.sleep(5)
            print("finished saving")


        
        
        print("sleeping 30")
        time.sleep(30)
        data = 5

        await browser.close()
        logging.info('Done!')

        return data


async def fetch_element(page, selector, max_tries=10):
    tries = 0
    el = None
    while el == None and tries < max_tries:
        el = await page.querySelector(selector)
        await page.waitFor(1000)

    return el

async def fetch_elements(page, selector, max_tries=10):
    tries = 0
    el = None
    while el == None and tries < max_tries:
        el = await page.querySelectorAll(selector)
        await page.waitFor(1000)

    return el

print(f"Creating Meter")

# meter = Meter(
#     email=os.getenv("EMAIL"),
#     password=os.getenv("PASSWORD"),
#     mfa_type=os.getenv("MFA_TYPE"),
#     mfa_secret=os.getenv("MFA_SECRET"),
#     account_uuid=os.getenv("ACCOUNT_UUID"),
#     meter_number=os.getenv("METER_NUMBER"),
#     site=os.getenv("SITE"),
#     browser_path="/usr/bin/chromium-browser"
#     # browser_path="/usr/bin/google-chrome-stable"
# )

# make sure to comment below out before pushing


import test
meter = Meter(
    email=test.email,
    password=test.password,
    mfa_type=test.mfa_type,
    mfa_secret=test.mfa_secret,
    account_uuid=test.account_uuid,
    meter_number=test.meter_number
)



print(f"Calling meter.last_read()..")
result = asyncio.get_event_loop().run_until_complete(meter.post_story())
