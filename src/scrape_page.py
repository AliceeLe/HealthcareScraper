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

doctor_id = "dnn_ctr422_TimKiemGPHD_UpdatePanel1"

def clean_name_role(a_content: str, row_data: list[str]):
    index = a_content.find('\n')
    if index != -1:  # If '\n' is found
        name = a_content[0:index]  # Extract and strip the name
        role = a_content[index+1:]  # Extract and strip the role
        row_data.append(name)
        role_index = role.find(next(filter(str.isalpha, role)))
        role_filtered = role[role_index:]
        new_role = role_filtered.replace('\n', '')  
        row_data.append(new_role)
    else: # If no \n
        row_data.append(a_content)

def process_row(row, hospital_info):
    columns = row.find_all('td')
    row_data = ast.literal_eval(hospital_info)
    for column in columns:
        if column.find('a'):
            a_content = column.find('a').get_text(strip=True)
            clean_name_role(a_content, row_data)
        else:
            row_data.append(column.get_text(strip=True))
    with open('src/csv/output.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(row_data)        
    return row_data

def scrape_table(page_source: str, hospital_info: str, wait) -> list[str]:
    try:
        time.sleep(3)
        soup = BeautifulSoup(page_source, 'html.parser')
        doctors_content = soup.find('div', id=doctor_id)    
        table_rows = doctors_content.find_all('tr', style="color:#003399;background-color:White;")

        last_row_data = None  # Initialize last_row_data
        for row in table_rows:
            row_data = process_row(row, hospital_info)
            last_row_data = row_data  # Update last_row_data with the current row data
        if last_row_data is not None:
            return int(last_row_data[4])  # Return the last row data after the loop
    except Exception as error:
        print("An exception occurred in scrape_page:", error)
        return None  # Return None in case of an exception
