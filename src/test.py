import pandas as pd
import csv
import ast
from openpyxl import Workbook
import csv

def create_excel():
    wb = Workbook()
    ws = wb.active
    with open('src/csv/output_organized.csv', 'r') as f:
        for row in csv.reader(f):
            ws.append(row)
    wb.save('medinet.xlsx')


def check_missing():
    try:
        # Load the CSV file
        df = pd.read_csv("src/csv/license.csv")
        
        # Extract the first column
        first_column = df.iloc[:, 0]
        
        # Define the range of values to check
        required_values = set(range(1, 930))
        
        # Get the unique values from the first column
        column_values = set(first_column.unique())
        
        # Check for missing values
        missing_values = required_values - column_values
        
        if missing_values:
            print(f"Missing values: {sorted(missing_values)}")
        else:
            print("All values from 1 to 500 are present in the first column.")
        
        return missing_values
    except FileNotFoundError:
        print(f"The file was not found.")
    except pd.errors.EmptyDataError:
        print("No data in the CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def reorganize_csv():
    df = pd.read_csv("src/csv/license.csv")
    df = df.sort_values(by=df.columns[0])
    df = df.drop_duplicates()
    df.to_csv('license_sorted.csv', index=False)
    print("Finish sorting")


def extract_addresses():
    addresses = []  # List to store addresses
    
    try:
        with open("src/csv/license_sorted.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row if there is one
            for row in reader:
                if row:
                    # Assuming 'hospital_info' is the third column
                    hospital_info = row[2]
                    # Evaluate the string representation of the list
                    info_list = ast.literal_eval(hospital_info)
                    # Append the address (second element of the list)
                    addresses.append(info_list[2])
    except FileNotFoundError:
        print(f"The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return addresses

def check_missing_output(address_list):
    try:
        # Load the CSV file
        df = pd.read_csv("src/csv/output.csv")
        
        # Extract the fourth column
        fourth_column = df.iloc[:, 3]
        
        # Define the range of values to check
        required_values = set(address_list)
        
        # Get the unique values from the fourth column
        column_values = set(fourth_column.unique())
        
        # Check for missing values
        missing_values = required_values - column_values
        
        if missing_values:
            print(len(missing_values))
            return missing_values
        else:
            print("All addresses are present in the fourth column.")
        
        return missing_values
    except FileNotFoundError:
        print(f"The file was not found.")
    except pd.errors.EmptyDataError:
        print("No data in the CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def filter_and_save_rows(address_list):
    """
    Filters rows from a CSV based on whether the address in the hospital_info column
    matches any address in the provided list and writes matching rows to a new CSV file.

    Parameters:
    address_list (list): List of addresses to filter by.
    """
    try:
        # Read the CSV file
        df = pd.read_csv("src/csv/license_sorted.csv", header=None)
        
        # Define a set for faster lookup
        address_set = set(address_list)
        
        # Filter rows where the address in hospital_info matches an address in the list
        def is_address_in_list(hospital_info_str):
            try:
                # Parse the hospital_info string as a list
                info_list = ast.literal_eval(hospital_info_str)
                # Get the address (second element of the list)
                address = info_list[2]
                return address in address_set
            except:
                # If parsing fails or the list is not as expected, skip this row
                return False

        # Apply the filtering function to the hospital_info column
        filtered_df = df[df[2].apply(is_address_in_list)]
        
        # Write the filtered DataFrame to a new CSV file
        filtered_df.to_csv("src/csv/missing.csv", index=False, header=False)
        print(f"Filtered rows have been written to missing.csv.")
        
    except FileNotFoundError:
        print(f"The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def organize_and_save_csv():
    try:
        # Load the CSV file
        df = pd.read_csv("src/csv/output.csv")   
        print("Column names:", df.columns)

        # # Convert the first (Page) and second (Button) columns to numeric, if they're not already
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
        df.iloc[:, 4] = pd.to_numeric(df.iloc[:, 4], errors='coerce')

        df = df.drop_duplicates()
        
        df_sorted = df.sort_values(['Page', 'Button', 'STT'], ascending=True)
        
        # Write the organized DataFrame to a new CSV file
        df_sorted.to_csv("src/csv/output_organized.csv", index=False)
        print(f"Data has been organized and saved to output_organized.csv")
        
    except FileNotFoundError:
        print(f"The file was not found.")
    except pd.errors.EmptyDataError:
        print("No data in the CSV file.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

# addresses = extract_addresses()
# missing = check_missing_output(addresses)
# filter_and_save_rows(missing)
# organize_and_save_csv()
# reorganize_csv()


def save_rows_with_100_in_fourth_column():
    try:
        # Load the CSV file
        df = pd.read_csv("src/csv/output_organized.csv", header=None)  # Adjust header usage as necessary
                
        fourth_column = df.iloc[:, 4]  
        
        # Convert all data in the fourth column to numeric, errors are coerced to NaN
        fourth_column_numeric = pd.to_numeric(fourth_column, errors='coerce')
        
        # Find rows where the fourth column has value 100
        rows_with_100 = df[fourth_column_numeric == 100]
        
        # Save these rows to a new CSV file
        rows_with_100.to_csv("src/csv/remaining.csv", index=False, header=None)
        
        print(f"Rows where the fourth column has value 100 have been saved to remaining.csv")
        return len(rows_with_100)
        
    except FileNotFoundError:
        print("The file was not found.")
        return 0
    except pd.errors.EmptyDataError:
        print("No data in the CSV file.")
        return 0
    except pd.errors.ParserError as pe:
        print(f"Error parsing CSV file: {pe}")
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

# save_rows_with_100_in_fourth_column()

def check_10():
    file_path = 'src/csv/license_sorted.csv'  # Replace with the path to your CSV file
    df = pd.read_csv(file_path)
    print("Columns in the DataFrame:", df.columns.tolist())

    # Count the number of rows for each license_id
    license_counts = df["page_num"].value_counts()

    # Filter license_ids that do not have 10 rows
    incomplete_license_ids = license_counts[license_counts != 10].index.tolist()

    res = []
    # Print the incomplete license_ids
    if incomplete_license_ids:
        print("Store page_ids do not have exactly 10 rows:")
        for license_id in incomplete_license_ids:
            res.append(license_id)
        print(len(res))
        res.sort()
        print(res)
        return res
    else:
        print("All license_ids have exactly 10 rows.")

def clean_repeating_rows():
    """
    Deletes repeating rows in a CSV file in place.
    
    Parameters:
    - file_path: str, path to the CSV file to be cleaned
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv('src/csv/license_sorted.csv')

    df_unique = df.drop_duplicates(subset='license_id', keep='last')

    df_unique.to_csv('src/csv/license_sorted.csv', index=False)
    
    print(f"Duplicate rows removed and cleaned CSV file saved to")

check_10()