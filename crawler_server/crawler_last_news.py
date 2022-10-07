import time

import pyodbc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from Model import config


def wait_elem(chrome, css_selector):
    WebDriverWait(chrome, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
    return


sqlConn = pyodbc.connect(config.db_connect, autocommit=True)
cursor = sqlConn.cursor()

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")

chrome = webdriver.Chrome(executable_path='C:\selenium_driver_chrome\95.0.4638.17\chromedriver', options=options)

big_num = 5012
while big_num < 5024:
    num = 6
    for i in range(0, 6):
        url = f'https://www.mohw.gov.tw/lp-{big_num}-1-{num}-20.html'
        print(num)
        num-=1
        if num <= 0:
            break
        chrome.get(url)

        wait_elem(chrome, '.list01')

        get_news_box = chrome.find_element_by_css_selector('.list01')
        get_news_list = get_news_box.find_elements_by_css_selector('li')

        list_new = []
        for elemt in get_news_list:
            data = {"url": "", "date": "", "new_name": ""}
            data["url"] = elemt.find_element_by_css_selector('a').get_attribute('href')
            data["date"] = elemt.find_element_by_css_selector('span').text
            data["new_name"] = elemt.find_element_by_css_selector('a').get_attribute('title')
            list_new.insert(0, data)
            print(data)
        time.sleep(2)
        for i in list_new:
            try:
                cursor.execute("""INSERT INTO
                Health_Fukube_News
                (Title, Url, Post_Date, Logtime)
                VALUES(?, ?, ?, GETDATE())""", i["new_name"], i["url"], i["date"])
            except Exception as e:
                print(e)
        time.sleep(2)
    big_num += 1
chrome.close()
chrome.quit()
exit(0)



