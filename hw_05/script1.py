import datetime, os, time
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

client = MongoClient('localhost', 27017)
db = client['selenium']
collection = db['mvideo']

datetime_current = datetime.datetime.now()
chromedriver = "/Users/paveltukin/teach/geekbrains/gb_data_collection/hw_05/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get("https://www.mvideo.ru/")

full_block = driver.find_elements_by_css_selector('.sel-hits-block')[1]
sel_hits_block2 = full_block.find_element_by_css_selector('.sel-hits-button-next')
time.sleep(2)

actions = ActionChains(driver)
actions.move_to_element(sel_hits_block2)

while True:
    try:
        time.sleep(2)
        sel_hits_block2.click()
    except:
        break

a_list = full_block.find_elements_by_css_selector('.c-product-tile-picture__holder a')

for a in a_list:
    item = {
        '_id': int(a.get_attribute('href').split('-')[-1]),
        'href': a.get_attribute('href'),
        'name': a.get_attribute('data-track-label'),
        'product_info': a.get_attribute('data-product-info')
    }

    try:
        collection.insert_one(item)
    except Exception as e:
        print("Уже есть такая запись. ", e)