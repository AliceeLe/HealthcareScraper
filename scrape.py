from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import csv

url = 'http://thongtin.medinet.org.vn/Gi%E1%BA%A5y-ph%C3%A9p-ho%E1%BA%A1t-%C4%91%E1%BB%99ng'

# IDs for elements
page_ids = [
"dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_1",
"dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_2",
"dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_3",
"dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_4",
"dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_5",
"dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_6",
]

link_dict = {
    "dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_0":"dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_0",
    "dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_1":"dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_1",
    "dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_2":"dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_2",
    "dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_3":"dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_3",
    "dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_4":"dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_4",
    "dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_5":"dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_5",
    "dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_6":"dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_6",
    "dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_7":"dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_7",
    "dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_8":"dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_8",
    "dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_9":"dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_9",
}

doctor_id = "dnn_ctr422_TimKiemGPHD_UpdatePanel1"

def clean_name_role(a_content: str, row_data: list[str]):
    index = a_content.find('\n')
    if index != -1:  # If '\n' is found
        name = a_content[0:index]  # Extract and strip the name
        role = a_content[index+1:]  # Extract and strip the role
        row_data.append(name)
        role_index= role.find(next(filter(str.isalpha, role)))
        role_filtered = role[role_index:]
        new_role = role_filtered.replace('\n', '')  
        row_data.append(new_role)
    else: # If no \n
        row_data.append(a_content)

def clean_data(row, button_num: int, hospital_id: str, hospital: str):
    columns = row.find_all('td')
    row_data = [button_num, hospital_id[-1], hospital]
    for column in columns:
        if column.find('a'):
            a_content = column.find('a').get_text(strip=True)
            clean_name_role(a_content, row_data)
        else:
            row_data.append(column.get_text(strip=True))
    return row_data

def scrape_table(page_source: str, button_num: int, link_id: str, hospital_id: str, hospital: str):
    try:
        # Use BeautifulSoup to parse the new page's source
        soup = BeautifulSoup(page_source, 'html.parser')
        doctors_content = soup.find('div', id=doctor_id)        
        table_rows = doctors_content.find_all('tr', style="color:#003399;background-color:White;")

        # Open a CSV file to write the data
        with open('output.csv','a') as file:
            writer = csv.writer(file)
                    
            for row in table_rows:
                row_data = clean_data(row, button_num, hospital_id, hospital)
                writer.writerow(row_data)
        print(f"Finish row {link_id}'") 
    except Exception as error:
        print("An exception occurred:", error) 

driver = webdriver.Chrome()

def scrape_links(page_id:str, button_num:int, n: int):
    try:
        for hospital_id, link_id in link_dict.items():
            driver.get(url)
            wait = WebDriverWait(driver, 5)

            if page_id == "dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_7":
                for i in range(n+1):
                    link_element = wait.until(EC.element_to_be_clickable((By.ID, page_id)))
                    link_element.click()
                    time.sleep(1)  
            elif page_id != "dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_1":
                link_element = wait.until(EC.element_to_be_clickable((By.ID, page_id)))
                link_element.click()

            # Parse the hospital info
            page_source = driver.page_source

            soup = BeautifulSoup(page_source, 'html.parser')
            hospital = soup.find('a', id = hospital_id).text
            print(hospital)

            ## CODE IF HOSPITAL_ID IS NOT THERE, USE LINK_ID
            try:
                link_element = wait.until(EC.element_to_be_clickable((By.ID, hospital_id)))
            except: 
                link_element = wait.until(EC.element_to_be_clickable((By.ID, link_id)))
            link_element.click()

            # Wait for the new page to load
            time.sleep(2)  

            # Now scrape the information from the new page
            page_source = driver.page_source
            scrape_table(page_source, button_num, link_id, hospital_id, hospital)
                
    except TimeoutException:
        print(f"Element with ID '{link_id}' was not found within 10 seconds.")
        pass

    finally:
        if page_id == "dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_7":
            page_id = page_id[:-1]+str(7+n)
        print(f"DONE BUTTON {page_id}'") 


for page_id in page_ids:
    scrape_links(page_id, int(page_id[-1]), 0)

for i in range(3):
    scrape_links("dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_7", 7+i, i)