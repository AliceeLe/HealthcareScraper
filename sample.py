from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import csv

"""
Bam vao tung button. Sau do thi store array cua so giay phep. Search so giay phep va scrape 
info thay vi bam 50 button.
Remaining: 
- Write function bam nut cuoi cung thay vi la bam nut 7 lien tuc 
- Bam nut ben trong tung trang neu so bac si > 100

Bug:
- If hospital doesnt have doctors, info will be taken from the old hospital 
"""

url = 'http://thongtin.medinet.org.vn/Gi%E1%BA%A5y-ph%C3%A9p-ho%E1%BA%A1t-%C4%91%E1%BB%99ng'
driver = webdriver.Chrome()

table_id = 'dnn_ctr422_TimKiemGPHD_grvGPHN'
input_search_id = 'dnn_ctr422_TimKiemGPHD_txtSoGiayPhepSearch'
button_search_id = 'dnn_ctr422_TimKiemGPHD_btnSearchGPHN'
hospital_id = 'dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_0'
license_click_id = 'dnn_ctr422_TimKiemGPHD_grvGPHN_btnSoGiayPhep_0'
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

def process_row(row, row_data):
    columns = row.find_all('td')
    row_data = row_data[:4]
    for column in columns:
        if column.find('a'):
            a_content = column.find('a').get_text(strip=True)
            clean_name_role(a_content, row_data)
        else:
            row_data.append(column.get_text(strip=True))
    with open('output.csv','a') as file:
        writer = csv.writer(file)
        print(row_data)
        writer.writerow(row_data)



def scrape_table(page_source: str, row_data: list[str]):
    try:
        # Use BeautifulSoup to parse the new page's source
        soup = BeautifulSoup(page_source, 'html.parser')
        doctors_content = soup.find('div', id=doctor_id)    
        table_rows = doctors_content.find_all('tr', style="color:#003399;background-color:White;")

        for row in table_rows:
            process_row(row, row_data)

    except Exception as error:
        print("An exception occurred:", error) 

def locate_table(page_id:str):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    table_content = soup.find('table', id=table_id)

    row_data = []
    table_dict = {}
    rows =   table_content.find_all('tr')
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
            # clean license string if len > 14
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
            
    print(table_dict)
    return table_dict

# Fix this 
def locate_button(page_id, n):
    wait = WebDriverWait(driver, 3)
    if page_id == "dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_7":
        for i in range(n+1):
            link_element = wait.until(EC.element_to_be_clickable((By.ID, page_id)))
            link_element.click()
            time.sleep(1)  
    elif page_id != "dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_1":
        link_element = wait.until(EC.element_to_be_clickable((By.ID, page_id)))
        link_element.click()

def search_from_license(license_id, driver, wait, table_dict, page_num):
    print("-------")
    print(license_id)
    # Locate the input field (by ID, name, or other selector)
    page_source = driver.page_source
    input_field = driver.find_element(By.ID, input_search_id)  
    input_field.clear()
    input_field.send_keys(license_id)
    time.sleep(1)  
    submit_button = driver.find_element(By.ID, button_search_id) 
    submit_button.click()
    time.sleep(2)  
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    row_data = table_dict.get(license_id)
    row_data.insert(0, page_num)
    print(row_data)

    try:
        link_element = wait.until(EC.element_to_be_clickable((By.ID, hospital_id)))
    except: 
        link_element = wait.until(EC.element_to_be_clickable((By.ID, license_click_id)))
    link_element.click()
    time.sleep(2)  
    page_source = driver.page_source 
    scrape_table(page_source, row_data)


def scrape_links_alternative(page_id: str, n: int):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        page_num = int(page_id[-1])
       ## Locate button  
        locate_button(page_id, n)

        table_dict = locate_table(page_id)  
        license_data = table_dict.keys()
        row_data = table_dict.values()
        print(license_data)
        print(row_data)

        ## From license_data, search 
        for license in license_data:
            search_from_license(license, driver, wait, table_dict, page_num)

    except TimeoutException:
        print(f"Element was not found within 10 seconds.")
        pass

scrape_links_alternative("dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_1", 1)
