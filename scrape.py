from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

url = 'http://thongtin.medinet.org.vn/Gi%E1%BA%A5y-ph%C3%A9p-ho%E1%BA%A1t-%C4%91%E1%BB%99ng'

# IDs for elements
page_id = "dnn_ctr422_TimKiemGPHD_rptPager_lnkPage_1"
link_ids = ["dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_0", 
"dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_1", 
"dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_2", 
"dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_3",
"dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_4", 
"dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_5", 
"dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_6",
"dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_7",
"dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_8",
"dnn_ctr422_TimKiemGPHD_grvGPHN_btnTenCoSo_9",
]
list_id = "chkDSNhanSu"
hospital_id = ""
doctor_id = "dnn_ctr422_TimKiemGPHD_UpdatePanel1"

# Set up the web driver
driver = webdriver.Chrome()

try:
    for link_id in link_ids:
        # Open the main page
        driver.get(url)

        # Wait until the link is clickable and click it
        wait = WebDriverWait(driver, 2)
        link_element = wait.until(EC.element_to_be_clickable((By.ID, link_id)))
        link_element.click()

        # Wait for the new page to load
        time.sleep(1)  # You may need to adjust this sleep time depending on the page load speed

        # Now scrape the information from the new page
        page_source = driver.page_source

        # Use BeautifulSoup to parse the new page's source
        soup = BeautifulSoup(page_source, 'html.parser')
        # hospital_content = soup.find('div', id = hospital_id)
        doctors_content = soup.find('div', id=doctor_id)
        table_rows = doctors_content.find_all('tr', style="color:#003399;background-color:White;")
        # Open a CSV file to write the data
        with open('output.csv','a') as file:
            writer = csv.writer(file)
            
            # Write the header row
            # writer.writerow(['STT', 'Họ tên', 'Vai trò', 'Quốc tịch', 'Số chứng chỉ', 'Phạm vi hành nghề', 'Ngày làm việc', 'Thời gian làm việc', 'ID'])

            for row in table_rows:
                # print(row.prettify())
                columns = row.find_all('td')
                row_data = []
                for column in columns:
                    if column.find('a'):
                        a_content = column.find('a').get_text(strip=True)
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
                    else:
                        row_data.append(column.get_text(strip=True))
                print(row_data)
                writer.writerow(row_data)
finally:
    driver.quit()

