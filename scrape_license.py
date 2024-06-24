import pandas as pd
import multiprocessing
import time
import csv
import ast
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from locate_button import compute_button

url = 'http://thongtin.medinet.org.vn/Gi%E1%BA%A5y-ph%C3%A9p-ho%E1%BA%A1t-%C4%91%E1%BB%99ng'
table_id = 'dnn_ctr422_TimKiemGPHD_grvGPHN'

def locate_table(page_id: str, driver):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    table_content = soup.find('table', id=table_id)

    row_data = []
    table_dict = {}
    rows = table_content.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        column_data = []
        for column in columns:
            if column.find('a'):
                a_content = column.find('a').get_text(strip=True)
                column_data.append(a_content)
            else:
                column_data.append(column.get_text(strip=True))
        
        if len(column_data) > 0:
            license = column_data[2]
            if len(license) > 14:
                license = license[:14]
            elif len(license) < 14:
                continue
            row_data = []
            row_data.append(column_data[0])
            row_data.append(column_data[1])
            row_data.append(column_data[3])
            table_dict[license] = row_data            

    return table_dict

def locate_button(n, driver):
    wait = WebDriverWait(driver, 3)
    template_page_id = 'dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_'
    arr = compute_button(n)
    # [0, 4, 1] approach 1: press button 11 0 times, press id 4
    # [5, 3, 2] approach 2: press button 12, then press button 1 5 times, then press id 3

    if arr[2] == 2:
        # press button 12
        link_element = wait.until(EC.element_to_be_clickable((By.ID, template_page_id+str(12))))
        link_element.click()
        time.sleep(1) 

    for i in range(arr[0]):
        button = 11 if arr[2] == 1 else 1
        link_element = wait.until(EC.element_to_be_clickable((By.ID, template_page_id+str(button))))
        link_element.click()
        time.sleep(1) 

    link_element = wait.until(EC.element_to_be_clickable((By.ID, template_page_id + str(arr[1]))))
    link_element.click()
    time.sleep(1) 

def scrape_license_page(n):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        locate_button(n, driver)
        table_dict = locate_table(n, driver)
        
        for key, value in table_dict.items():
            with open("license_new.csv", "a") as outfile:
                writer = csv.writer(outfile)
                writer.writerow([n, key, value])
    except TimeoutException:
        print(f"Element was not found within 10 seconds.")
    finally:
        driver.quit()
