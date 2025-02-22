import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def purchase(driver, listing):
    driver.find_element(By.XPATH, '/html/body/div[6]/div/div[7]/table/tbody/tr[{}]/td[6]/a'.format(listing+2)).click() #used to purchase
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'i_Btn pay-btn')))
        driver.find_element(By.CLASS_NAME, 'i_Btn pay-btn').click()
        print('success')
    except TimeoutException:
        print("Loading took too much time!")

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ask_seller')))
        driver.find_element(By.ID, 'ask_seller').click()
        print('success')
    except TimeoutException:
        print("Loading took too much time!")

    time.sleep(5)