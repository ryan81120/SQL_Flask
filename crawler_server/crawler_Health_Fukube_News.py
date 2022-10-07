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


def crawler_news():
    try:
        flag = False
        sqlConn = pyodbc.connect(config.db_connect, autocommit=True)
        cursor = sqlConn.cursor()

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")

        chrome = webdriver.Chrome(executable_path='C:\selenium_driver_chrome\96.0.4664.45\chromedriver', options=options)

        url = f'https://www.mohw.gov.tw/mp-1.html'
        chrome.get(url)

        wait_elem(chrome, '.tabContent')

        get_news_box = chrome.find_element_by_css_selector('.tabContent')
        get_news_list = get_news_box.find_elements_by_css_selector('li')

        list_new = []
        for elemt in get_news_list:
            data = {"url": "", "date": "", "new_name": ""}
            data["url"] = elemt.find_element_by_css_selector('a').get_attribute('href')
            data["date"] = elemt.find_element_by_css_selector('a span').text
            data["new_name"] = elemt.find_element_by_css_selector('a').text.replace(data["date"], "")
            list_new.insert(0, data)
            print(data)

        for i in list_new:
            try:
                cursor.execute("""
                SELECT 
                [id] ,[Title] ,[Url] ,[Post_Date] ,[Logtime]
                FROM [Hospital].[dbo].[Health_Fukube_News]
                WHERE Title = ? AND Url = ?
                """, i["new_name"], i["url"])
                new_log = cursor.fetchone()
                if new_log is None:
                    cursor.execute("""INSERT INTO
                    Health_Fukube_News
                    (Title, Url, Post_Date, Logtime)
                    VALUES(?, ?, ?, GETDATE())""", i["new_name"], i["url"], i["date"])
            except Exception as e:
                print(e)
        flag = True
    except Exception as e:
        print(e)
    finally:
        time.sleep(2)
        chrome.close()
        chrome.quit()
        return flag