#Note: Buff163 does not release its statistics on rate limits, but upon testing, a total of 3 scrapers at a time works best
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from executeOrder import purchase
import json
import time
import re
import os
import threading
import pickle
import sys

# The notifier function
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

def obtainItems(request, driver, maximumFloat, maximumPrice): # obtain list of 10 items wear values and prices for the links found in json file. Returns true if match is found

    driver.get(request) # driver configs
    time.sleep(0.5)
    cookies = pickle.load(open("cookies.pkl", "rb")) # enable cookies
    for cookie in cookies:
        driver.add_cookie(cookie)
    isNamed = True
    try:
        print(driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/div[2]/div[1]/h1').text,':\n')
    except NoSuchElementException:
        print('pass')
        isNamed = False
    offset = 0
    for i in range(10):

        while True:
            try:
                wear = driver.find_element(
                    By.XPATH, '/html/body/div[6]/div/div[7]/table/tbody/tr[{}]/td[3]/div/div[1]/div[1]'.format(i+2+offset))
                # consistent html behavior across different item links for CS:GO
                price = driver.find_element(
                    By.XPATH, '/html/body/div[6]/div/div[7]/table/tbody/tr[{}]/td[5]/div[1]/strong'.format(i+2+offset))
            except NoSuchElementException:
                print("could not locate item")
                try:
                    column = driver.find_element(
                        By.XPATH, '/html/body/div[6]/div/div[7]/table/tbody/tr[{}]'.format(i+2+offset))
                    objectclass = column.get_attribute("class")
                    if objectclass[0] == "d":
                        offset = offset+1
                    continue
                except NoSuchElementException:
                    driver.get(request)
                    time.sleep(0.5)
                    continue
            weartext = float(''.join(c for c in wear.text if c.isdigit() or c=='.'))
            print("Listing {}".format(i+1))
            print(price.text)
            print("Float:", weartext,"\n")
            print("Threads running:", threading.active_count())
            price = float(price.text[1:])
            print("checking if {} is less than {}".format(price,maximumPrice))
            if (weartext < maximumFloat) and (price<maximumPrice):
                notify("Buff Scraper", "An item has been found that matches your criteria:  {} \n{}"
                       .format("Listing {}".format(i+1), "Float: {}".format(weartext)))
                purchase(driver, i+offset)
            break
    driver.quit

class ScrapeThread(threading.Thread):
    def __init__(self, scrapernumber):
        threading.Thread.__init__(self)
        self.scrapernumber = scrapernumber
    def run(self):
        scrapeCount = 'scraper' + str(self.scrapernumber)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        time.sleep(1)
        while True:
            for dicto in data[scrapeCount]:
                link = dicto["link"]
                price = float(dicto["price"])
                maximumFloat = float(dicto["float"])
                obtainItems(link, driver, maximumFloat, price)

def scrape(firstScraper, lastScraper):
    threads = []

    for scrapeNum in range(firstScraper, lastScraper+1):
        t = ScrapeThread(scrapeNum)
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

f = open('./buff.json')
data = json.load(f)

if len(sys.argv) != 4:
    print('Please enter the correct number of arguments')
    pass
else:
    scrape(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))

# Note: if you want an example of a function run, uncomment this:
scrape(1, 2)

# add readme.md
