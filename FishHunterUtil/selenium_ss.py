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

def screenshot(url, driver="firefox", save_to="test_ss.png", javascript_enable=True, max_retry=5):
    web_driver = None
    if max_retry <= 0:
        # create black image
        img = Image.new("RGB", (1920, 1080), (0, 0, 0))
        img.save(save_to)

        return
    
    try:
        if driver == "firefox":
            web_driver = init_firefox_driver(javascript_enable=javascript_enable)
        elif driver == "chrome":
            web_driver = init_chrome_driver(javascript_enable=javascript_enable)

        web_driver.set_page_load_timeout(5)
        web_driver.maximize_window()
        web_driver.set_window_size(1920, 1080)

        print(">> Start navigating to {}".format(url))
        web_driver.get(url)
        print(">> Navigate DONE~")

        print("Delay 5 sec")
        # delay 5 seconds
        time.sleep(5)
        

        print(">> Start taking screenshot")
        ss = web_driver.get_screenshot_as_png()
        print(">> Screenshot taken")

        # convert to jpg
        img = Image.open(BytesIO(ss))
        img = img.convert("RGB")
        img.save(save_to)

        web_driver.quit()
        return
    except Exception as ex:
        print(ex)
        print(">> Error, retrying...")
        try: web_driver.quit()
        except: pass
        return screenshot(url, driver=driver, save_to=save_to, javascript_enable=javascript_enable, max_retry=max_retry-1)

if __name__ == "__main__":
    screenshot("file:///C:/code/research/Download/643ad03f583b2ca2b39c63a1/index.html", save_to="test_ss.jpg", driver="firefox", javascript_enable=True)