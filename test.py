import pandas as pd

def reorganize_csv():
    try:
        # Load the CSV file
        df = pd.read_csv("license_new.csv")
        
        # Sort the DataFrame by the first column (index 0)
        df_sorted = df.sort_values(by=df.columns[0], ascending=True)
        
        # Save the sorted DataFrame back to a CSV file (optional)
        df_sorted.to_csv("license_new_sorted.csv", index=False)
        
        return df_sorted
    except FileNotFoundError:
        print(f"The file was not found.")
    except pd.errors.EmptyDataError:
        print("No data in the CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
sorted_df = reorganize_csv()
if sorted_df is not None:
    print(sorted_df)
