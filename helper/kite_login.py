from time import sleep

from kiteconnect import KiteConnect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

API_KEY = ""
API_SECRET = ""
USER_ID = ""
PASSWORD = ""
PIN = ""


def generate_access_token():
    kite = KiteConnect(api_key=API_KEY)

    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(kite.login_url())

    sleep(1)

    # input username
    user = driver.find_element(By.XPATH, "//input[@type = 'text']")
    user.send_keys(USER_ID)

    # input password
    pwd = driver.find_element(By.XPATH, "//input[@type = 'password']")
    pwd.send_keys(PASSWORD)

    # click on login
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    sleep(1)

    # input pin
    pin = driver.find_element(By.XPATH, "//input[@type = 'password']")
    pin.send_keys(PIN)

    # click on continue
    driver.find_element(By.XPATH, "//button[@type = 'submit']").click()

    sleep(2)

    current_url = driver.current_url
    driver.close()

    initial_token = current_url.split('request_token=')[1]
    request_token = initial_token.split('&')[0]

    # Access Token
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    return data['access_token']


def get_historical_data(instrument, from_date, to_date, interval):
    kite = KiteConnect(api_key=API_KEY)
    access_token = generate_access_token()
    kite.set_access_token(access_token)

    return kite.historical_data(instrument, from_date, to_date, interval)


def get_all_instruments():
    kite = KiteConnect(api_key=API_KEY)
    access_token = generate_access_token()
    kite.set_access_token(access_token)
    print(kite.instruments())

# get_all_instruments()
