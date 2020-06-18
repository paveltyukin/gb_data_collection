import datetime, os, time
from pymongo import MongoClient
from selenium import webdriver

client = MongoClient('localhost', 27017)
db = client['selenium']
collection = db['emails']
datetime_current = datetime.datetime.now()

chromedriver = "/Users/paveltukin/teach/geekbrains/gb_data_collection/hw_05/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get("https://mail.ru")

login = driver.find_element_by_id('mailbox:login')
login.send_keys('***')
time.sleep(1)

button_login = driver.find_element_by_css_selector('.mailbox__row.mailbox__row_.i-clearfix input.o-control')
print(button_login)
button_login.click()
time.sleep(1)

password = driver.find_element_by_id('mailbox:password')
password.send_keys('***')
password.submit()

time.sleep(4)
letter_link_div = driver.find_element_by_css_selector('div.dataset__items')
a_link = letter_link_div.find_elements_by_css_selector('a')[3]
time.sleep(4)
driver.get(a_link.get_attribute('href'))

while True:
    try:
        time.sleep(2)
        button_next = driver.find_element_by_class_name('portal-menu-element_next')
        button_next.click()
        time.sleep(5)

        letter = driver.find_element_by_css_selector('.thread__letter_single')

        item = {
            'letter_title': driver.find_element_by_css_selector('.thread__subject_pony-mode').text,
            'letter_date': driver.find_element_by_css_selector('.letter__date').text,
            'letter_author': driver.find_element_by_css_selector('.letter__author span').get_attribute('title'),
            'letter_text': driver.find_element_by_css_selector('.letter__body').text,
            'date_now': datetime_current
        }

        collection.insert_one(item)
        time.sleep(2)
    except Exception as e:
        print("Письма закончились. ", e)
        break