from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import os
import time

def init_firefox_driver(javascript_enable=True):
    from selenium.webdriver.firefox.options import Options

    options = Options()

    # headless
    options.add_argument('-headless')

    # encoding to utf-8
    options.set_preference("intl.accept_languages", "en-US, en")

    if javascript_enable == False:
        options.set_preference("javascript.enabled", False)

    if os.name == 'posix':
        options.binary = "/opt/firefox/./firefox"
    else:
        options.binary = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

    driver = webdriver.Firefox(options=options)

    return driver

def init_chrome_driver(javascript_enable=True):
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # disable GPU
    options.add_argument('--disable-gpu')

    # disable cors
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('--allow-file-access-from-files')
    options.add_argument('--allow-file-access')
    options.add_argument('--allow-cross-origin-auth-prompt')

    if javascript_enable == False:
        options.add_argument('--disable-javascript')
        prefs = {}
        prefs["webkit.webprefs.javascript_enabled"] = False
        prefs["profile.content_settings.exceptions.javascript.*.setting"] = 2
        prefs["profile.default_content_setting_values.javascript"] = 2
        prefs["profile.managed_default_content_settings.javascript"] = 2

        options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options, desired_capabilities=DesiredCapabilities.CHROME)

    return driver

def screenshot(url, driver="firefox", save_to="test_ss.png", javascript_enable=True):
    driver = None
    while True:
        try:
            if driver == "firefox":
                driver = init_firefox_driver(javascript_enable=javascript_enable)
            elif driver == "chrome":
                driver = init_chrome_driver(javascript_enable=javascript_enable)

            driver.maximize_window()
            driver.set_window_size(1920, 1080)

            print(">> Start navigating to {}".format(url))
            driver.get(url)
            print(">> Navigate DONE~")

            print("Delay 5 sec")
            # delay 5 seconds
            time.sleep(5)
            

            print(">> Start taking screenshot")
            ss = driver.get_screenshot_as_png()
            print(">> Screenshot taken")

            # convert to jpg
            img = Image.open(BytesIO(ss))
            img = img.convert("RGB")
            img.save(save_to)

            driver.quit()
        except Exception as ex:
            print(ex)
            print(">> Error, retrying...")
        finally:
            try: driver.quit()
            except: pass

if __name__ == "__main__":
    screenshot("https://www.whatismybrowser.com/detect/is-javascript-enabled", save_to="test_ss.jpg", driver="firefox", javascript_enable=True)