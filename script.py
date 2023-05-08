from selenium import webdriver
from selenium.webdriver import Keys
import time
from selenium.webdriver.chrome.service import Service as ChromeService

# driver = webdriver.Chrome(service=ChromeService(executable_path='../chromedriver'))
driver = webdriver.Firefox()


def login():
    try:

        driver.get("https://www.reddit.com/login")
        username_field = driver.find_element("css selector", "#loginUsername")
        password_field = driver.find_element("css selector", "#loginPassword")

        # enter your login credentials
        username_field.send_keys("Broken-Back-16")
        password_field.send_keys("@Uday1601")

        # submit the login form
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)
    except Exception as e:
        print(e)
        # quit the driver only if there is an error
        driver.quit()


def post_screenshot():
    driver.get("https://www.reddit.com/r/AskReddit/comments/v35pc0/which_cheap_and_massproduced_item_is_stupendously/")
    post_title = driver.find_element(value="t3_v35pc0")
    post_title.screenshot('./post.png')


login()
post_screenshot()
driver.quit()
