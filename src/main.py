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
from test import check_10 

url = 'http://thongtin.medinet.org.vn/Gi%E1%BA%A5y-ph%C3%A9p-ho%E1%BA%A1t-%C4%91%E1%BB%99ng'
table_id = 'dnn_ctr422_TimKiemGPHD_grvGPHN'
input_search_id = 'dnn_ctr422_TimKiemGPHD_txtSoGiayPhepSearch'
button_search_id = 'dnn_ctr422_TimKiemGPHD_btnSearchGPHN'
hospital_id = 'dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_0'
license_click_id = 'dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_0'
doctor_id = "dnn_ctr422_TimKiemGPHD_UpdatePanel1"
next_button_id = "dnn_ctr422_TimKiemGPHD_rptPagerNhanSu_lnkPageNhanSu_2"


def turn_page(page_source, value, wait, driver, num):
    # last_num = scrape_table(page_source, value, wait)
    # while last_num is not None and last_num % 100 == 0:
        try:
            print("New page turned")
            # num_page = math.floor(last_num/100)
            id_11 = "dnn_ctr422_TimKiemGPHD_rptPagerNhanSu_lnkPageNhanSu_11" 
            id_next_page = "dnn_ctr422_TimKiemGPHD_rptPagerNhanSu_lnkPageNhanSu_" + str(num)
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

            # link_element = wait.until(EC.element_to_be_clickable((By.ID, id_11)))
            # link_element.click()
            # print("Click next button")
            # time.sleep(2) 

            link_element = wait.until(EC.element_to_be_clickable((By.ID, id_next_page)))
            link_element.click()
            print("Click next button")
            time.sleep(2) 

            page_source = driver.page_source 
            scrape_table(page_source, value, wait)
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
        try:
            # turn_page(page_source, value, wait, driver, 2)
            # turn_page(page_source, value, wait, driver, 3)
            # turn_page(page_source, value, wait, driver, 4)
            # turn_page(page_source, value, wait, driver, 5)
            # # turn_page(page_source, value, wait, driver, 6)
            # for i in range(8):
            #     turn_page(page_source, value, wait, driver, 7)
            turn_page(page_source, value, wait, driver, 8)
            # turn_page(page_source, value, wait, driver, 9)
            # turn_page(page_source, value, wait, driver, 10)
            # turn_page(page_source, value, wait, driver, 11)
        except Exception as e:
            print(f"An error occurred: {e}")

    finally:
        driver.quit()


def scrape_license_parallel(page_start, page_end):
    if __name__ == '__main__':
        page_numbers = list(range(page_start, page_end + 1))
        with multiprocessing.Pool(processes=4) as pool:
            pool.map(scrape_license_page, page_numbers)
        print(f"Scraping completed for pages {page_start} to {page_end}")

def scrape_license_missing_array():
    if __name__ == '__main__':
        # modify this part
        page_numbers = check_10()
        with multiprocessing.Pool(processes=4) as pool:
            pool.map(scrape_license_page, page_numbers)
        print(f"Scraping completed for missing array")

def license_to_dict(row_start, row_end):
    try:
        # Read the CSV file
        df = pd.read_csv("missing.csv", header=None)
        
        # Slice the DataFrame from row_start to row_end (inclusive)
        sliced_df = df.iloc[row_start:row_end+1]
        
        # Process the DataFrame to create a dictionary as specified
        key_value_dict = {}
        for index, row in sliced_df.iterrows():
            key = row[1]  
            value_list = ast.literal_eval(row[2])  # Evaluate the string list in the third column
            value_list.insert(0, str(row[0]))
            value = str(value_list)
            key_value_dict[key] = value
        
        return key_value_dict
    except FileNotFoundError:
        print("The file was not found.")
    except pd.errors.EmptyDataError:
        print("No data in the CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_key_value_pair(pair):
    try:
        key, value = pair
        search_from_license(key, value)
    except Exception as e:
        print(f"An error occurred in process_key_value_pair: {e}")

def process_license_dict_in_parallel(license_dict, num_processes=4):
    if __name__ == '__main__':
        try:
            if license_dict:
                with multiprocessing.Pool(processes=num_processes) as pool:
                    pool.map(process_key_value_pair, license_dict.items())
                print("Processing completed for all key-value pairs.")
            else:
                print("License dictionary is empty or not loaded properly.")
        except Exception as e:
            print(f"An error occurred in process_license_dict_in_parallel: {e}")
                
if __name__ == '__main__':
    try:
        # scrape_license_parallel(922, 932)
        scrape_license_missing_array()

        # key = "351/BYT-GPHĐ"
        # value = "['877','9', 'Bệnh viện Đa khoa Tâm Anh Quận 8', '316C Phạm Hùng, Phường 5, Quận 8, TP Hồ Chí Minh']"
        # search_from_license(key, value)
        # license_dict = license_to_dict(1001, 2113)
        # process_license_dict_in_parallel(license_dict)
    except Exception as e:
        print(f"An error occurred in main: {e}")

