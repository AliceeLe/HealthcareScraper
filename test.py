import pandas as pd

def check_missing():
    try:
        # Load the CSV file
        df = pd.read_csv("license.csv")
        
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
    df = pd.read_csv("license.csv")

    df = df.sort_values(by=df.columns[0])

    df = df.drop_duplicates()

    df.to_csv('license_sorted.csv', index=False)

    print("Finish sorting")

reorganize_csv()