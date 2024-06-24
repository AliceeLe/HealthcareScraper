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
from scrape_license import scrape_license_page
from scrape_page import scrape_table

url = 'http://thongtin.medinet.org.vn/Gi%E1%BA%A5y-ph%C3%A9p-ho%E1%BA%A1t-%C4%91%E1%BB%99ng'
table_id = 'dnn_ctr422_TimKiemGPHD_grvGPHN'
input_search_id = 'dnn_ctr422_TimKiemGPHD_txtSoGiayPhepSearch'
button_search_id = 'dnn_ctr422_TimKiemGPHD_btnSearchGPHN'
hospital_id = 'dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_0'
license_click_id = 'dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_0'
doctor_id = "dnn_ctr422_TimKiemGPHD_UpdatePanel1"
next_button_id = "dnn_ctr422_TimKiemGPHD_rptPagerNhanSu_lnkPageNhanSu_2"


def turn_page(page_source, value, wait, driver):
    last_num = scrape_table(page_source, value, wait)
    while last_num is not None and last_num % 100 == 0:
        try:
            print("New page turned")
            num_page = math.floor(last_num/100)
            id_next_page = "dnn_ctr422_TimKiemGPHD_rptPagerNhanSu_lnkPageNhanSu_"+str(num_page+1)
            print(id_next_page)
            # Click the checkbox before scrolling down
            checkbox = driver.find_element(By.ID, 'chkDSNhanSu')
            if not checkbox.is_selected():
                checkbox.click()
            time.sleep(1)  # Wait for any dynamic content to load
            print("Click checkbox")

            # Scroll down to find next_button_id
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # Wait for the page to load and the element to appear

            # Ensure the element is in view
            next_button = driver.find_element(By.ID, id_next_page)
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)  # Give time for any dynamic content to load

            link_element = wait.until(EC.element_to_be_clickable((By.ID, id_next_page)))
            link_element.click()
            print("Click next button")
            time.sleep(2) 

            page_source = driver.page_source 
            last_num = scrape_table(page_source, value, wait)
        except TimeoutException:
            print(f"Element was not found within 10 seconds.")
        except Exception as e:
            print(f"An error occurred in turn_page: {e}")


def search_from_license(key, value):
    driver = webdriver.Chrome()
    try:
        print("________")
        print(key)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        input_field = driver.find_element(By.ID, input_search_id)
        input_field.clear()
        input_field.send_keys(key)
        time.sleep(1)
        
        submit_button = driver.find_element(By.ID, button_search_id)
        submit_button.click()
        time.sleep(1)
        
        try:
            link_element = wait.until(EC.element_to_be_clickable((By.ID, hospital_id)))
        except: 
            link_element = wait.until(EC.element_to_be_clickable((By.ID, license_click_id)))
        link_element.click()
        time.sleep(2)
        
        page_source = driver.page_source 
        scrape_table(page_source, value, wait)

    finally:
        driver.quit()


def scrape_license_parallel(page_start, page_end):
    if __name__ == '__main__':
        page_numbers = list(range(page_start, page_end + 1))
        with multiprocessing.Pool(processes=4) as pool:
            pool.map(scrape_license_page, page_numbers)
        print(f"Scraping completed for pages {page_start} to {page_end}")

def license_to_dict():
    try:
        df = pd.read_csv("license_new.csv")
        key_value_dict = pd.Series(df.iloc[:, 2].values, index=df.iloc[:, 1]).to_dict()
        return key_value_dict
    except FileNotFoundError:
        print(f"The file was not found.")
    except pd.errors.EmptyDataError:
        print("No data in the CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_key_value_pair(pair):
    key, value = pair
    search_from_license(key, value)

def process_license_dict_in_parallel(license_dict, num_processes=4):
    if __name__ == '__main__':
        if license_dict:
            with multiprocessing.Pool(processes=num_processes) as pool:
                pool.map(process_key_value_pair, license_dict.items())
            print("Processing completed for all key-value pairs.")
        else:
            print("License dictionary is empty or not loaded properly.")

if __name__ == '__main__':
    scrape_license_parallel(251, 500)
    # license_dict = license_to_dict()
    # process_license_dict_in_parallel(license_dict)

