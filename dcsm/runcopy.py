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
    """A smart energy meter of ConEdison or Orange and Rockland Utility.

    Attributes:
        email: A string representing the email address of the account
        password: A string representing the password of the account
        mfa_type: Meter.MFA_TYPE_SECURITY_QUESTION or Meter.MFA_TYPE_TOTP
        mfa_secret: A string representing the multiple factor authorization secret
        account_uuid: A string representing the account uuid
        meter_number: A string representing the meter number
        site: Optional. Either `coned` (default, for ConEdison) or `oru` (for Orange and Rockland Utility)
        loop: Optional. Specific event loop if needed. Defaults to creating the event loop.
        browser_path: Optional. Specific chromium browser installation. Default to the installation that comes with pyppeteer.
    """

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


    async def last_read(self):
        """Return the last meter read value and unit of measurement"""
        try:
            await self.browse()

            # Reassign to fit legacy code
            return "pizza is the answer"

        except Exception as e:
            print(e)
            raise MeterError("Error requesting meter data")

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
        page = await browser.newPage()

        # Go to instagram
        # await page.goto('https://medium.com/analytics-vidhya/run-javascript-from-python-c0fe8f8aeb1e', {'waitUntil' : 'domcontentloaded'})


        page.on(
            'dialog',
            lambda dialog: asyncio.ensure_future(close_dialog(dialog, browser))
        )
        await page.evaluate('() => alert("1")')

        # Sleep so loading can finish
        time.sleep(4)

async def close_dialog(dialog, browser):
    print(dialog.message)
    await dialog.dismiss()
    await browser.close()

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
tester = asyncio.get_event_loop().run_until_complete(meter.last_read())



# message = {'startTime': startTime, 'endTime': endTime, 'value': value, 'uom': uom}

# print(f"message: {message}")

# mqtthost = os.getenv("MQTT_HOST")
# mqttuser = os.getenv("MQTT_USER")
# mqttpass = os.getenv("MQTT_PASS")

# print(f"Connecting to mqtt {mqtthost} as {mqttuser}")

# mqttc = mqtt.Client("oru_meter_reader")
# mqttc.username_pw_set(username=mqttuser, password=mqttpass)
# mqttc.connect(mqtthost)

# print(f"Publishing to mqtt")

# print(f"Publishing electric_meter/value: {value}")
# mqttc.publish('electric_meter/value', value, retain=True)
# time.sleep(1)

# print(f"Publishing electric_meter/uom: {uom}")
# mqttc.publish('electric_meter/uom', uom, retain=True)
# time.sleep(1)

# print(f"Publishing electric_meter/startTime: {startTime}")
# mqttc.publish('electric_meter/startTime', startTime, retain=True)
# time.sleep(1)

# print(f"Publishing electric_meter/endTime: {endTime}")
# mqttc.publish('electric_meter/endTime', endTime, retain=True)
# time.sleep(1)

# print(f"Publishing electric_meter/message: {json.dumps(message)}")
# mqttc.publish('electric_meter/message', json.dumps(message), retain=True)
# time.sleep(1)

# print(f"Disconnectig from mqtt")
# mqttc.disconnect()

# print(f"DONE\n\n")
