from Helpers.Base import Base 
from utilities.readProperties import ReadConfig
import time
import pandas as pd
from utilities.reportScreenshot import add_screenshot
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot
from Helpers.Base import Base 
import json
import time

class Excel_HelperFunctions:

    def __init__(self,driver,extra):
        self.driver = driver
        self.extra = extra
        self.base = Base(self.driver)
        self.logger = LogGen.loggen()
        # instantiate the logScreenshot class
        self.LogScreenshot = cLogScreenshot(self.driver,self.extra)

    def enter_data_from_excel(self,excel_path, config_path):
        # Read configuration file
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Read data from the Excel file
        dataFile = pd.read_excel(excel_path)

        # Iterate through each feature in the configuration
        for feature, mapping in config.items():
            # Iterate through each row in the dataframe
            for index, row in dataFile.iterrows():
                try:
                    # Iterate through each column in the row
                    for column, textbox_id in mapping.items():
                        # Check if the column exists in the dataframe
                        if column in dataFile.columns:
                            # Retrieve the data for the column
                            data = row[column]
                            # Enter the data into the text box (replace this with your actual code to input data)
                            self.enter_data_into_textbox(textbox_id, data)
                            # Log successful input
                            print(f"Data '{data}' entered successfully for column '{column}' in row {index+1} for feature '{feature}'.")
                except Exception as e:
                    # Log error if data entry fails
                    print(f"Error occurred while entering data for row {index+1} for feature '{feature}': {e}")

    def load_data_from_spreadsheet(file_path, sheet_name):
        """
        Load data from a spreadsheet file into a pandas DataFrame.
        """
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df

    def verify_key_value_pairs(app_data, spreadsheet_data, key_column):
        """
        Verify key-value pairs between application data and spreadsheet data based on a specific key column.
        """
        # Ensure the key column is present in both datasets
        if key_column not in app_data.columns or key_column not in spreadsheet_data.columns:
            raise ValueError(f"Key column '{key_column}' not found in both datasets")

        # Set the key column as the index for quick lookup
        app_data.set_index(key_column, inplace=True)
        spreadsheet_data.set_index(key_column, inplace=True)

        # Iterate over each row in the application data and compare values with the spreadsheet data
        for index, app_row in app_data.iterrows():
            if index not in spreadsheet_data.index:
                print(f"Key '{index}' not found in spreadsheet data")
                continue
            
            spreadsheet_row = spreadsheet_data.loc[index]
            
            # Compare values for each column (key) between the two datasets
            for column in app_data.columns:
                if app_row[column] != spreadsheet_row[column]:
                    print(f"Key '{index}', Column '{column}': Application value '{app_row[column]}' does not match Spreadsheet value '{spreadsheet_row[column]}'")

    # Example usage
            # if __name__ == "__main__":
            #     # Load application data (assuming it's already in a pandas DataFrame)
            #     app_data = pd.DataFrame({
            #         'Key': ['A', 'B', 'C'],
            #         'Value1': [10, 20, 30],
            #         'Value2': ['X', 'Y', 'Z']
            #     })

            #     # Load spreadsheet data from an Excel file
            #     spreadsheet_file_path = 'path/to/spreadsheet.xlsx'
            #     spreadsheet_sheet_name = 'Sheet1'
            #     spreadsheet_data = load_data_from_spreadsheet(spreadsheet_file_path, spreadsheet_sheet_name)

            #     # Define the key column to use for verification
            #     key_column = 'Key'

            #     # Verify key-value pairs between application data and spreadsheet data
            #     try:
            #         verify_key_value_pairs(app_data, spreadsheet_data, key_column)
            #     except ValueError as e:
            #         print(e)
    def float_equal(a, b, tolerance=1e-9):
        """Check if two floating-point numbers are approximately equal."""
        return abs(a - b) <= tolerance
    
    def compare_with_precision(excel_value, webpage_value, precision=3):
        """Compare two numeric values with specified decimal precision."""
        if isinstance(excel_value, (int, float)) and isinstance(webpage_value, (int, float)):
            # Round both values to the specified precision
            excel_rounded = round(float(excel_value), precision)
            webpage_rounded = round(float(webpage_value), precision)
            # Compare rounded values
            return excel_rounded == webpage_rounded
        else:
            # For non-numeric values, do exact comparison
            return excel_value == webpage_value

        
    def getalltheKeyValuepairofPage(self, Key_xpath, Value_Xpath):
        try:
            # Wait for some time to ensure elements are loaded
            time.sleep(10)
            
            # Find all key elements using the provided Key_xpath
            key_elements = self.base.findElements("Keyxpath")
            ListofKeys = [element.text for element in key_elements]

            # Find all value elements using the provided Value_Xpath
            value_elements = self.base.findElements("Valuexpath")
            ListofValues = [element.text for element in value_elements]

            # Filter out keys that do not have corresponding values
            filtered_key_value_pairs = {}

            for key, value in zip(ListofKeys, ListofValues):
                if value.strip():  # Check if the value is not empty or only whitespace
                    filtered_key_value_pairs[key] = str(value)
            
            # Convert ListofValues to a single string
            values_string = ', '.join(filtered_key_value_pairs.values())

            # Print the extracted key-value pairs (optional)
            print("Here you are for all Key Value Pairs @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("Extracted Key-Value Pairs:")
            for key, value in filtered_key_value_pairs.items():
                print(f"{key}: {value}")
            return filtered_key_value_pairs
        
        except Exception as e:
            print(f"Error occurred while extracting key-value pairs: {e}")
            return None  # Return None or handle the error as needed

        
    def compare_ExcelwithWebpage_Dict(key_value_pairs, test_data_file):
    
            dict1=test_data_file
            dict2=key_value_pairs

            def normalize_key(key):
                """Normalize a key by removing spaces and converting to lowercase."""
                return key.replace(' ', '').lower()

            matches = []
            mismatches = []

            # Normalize keys in both dictionaries
            normalized_dict1 = {normalize_key(key): value for key, value in dict1.items()}
            normalized_dict2 = {normalize_key(key): value for key, value in dict2.items()}

            # Get the intersection of keys that exist in both dictionaries
            common_keys = set(normalized_dict1.keys()).intersection(set(normalized_dict2.keys()))

            # Iterate over common keys
            for key in common_keys:
                value1 = normalized_dict1[key]
                value2 = normalized_dict2[key]

                # Convert values to string for comparison
                str_value1 = str(value1) if isinstance(value1, list) else str(value1)
                str_value2 = str(value2) if isinstance(value2, list) else str(value2)

                # Compare values
                if str_value1 == str_value2:
                    matches.append((key, value1, value2))
                else:
                    mismatches.append((key, value1, value2))

            # Check for keys in normalized_dict1 that are missing in normalized_dict2
            missing_keys_in_dict2 = set(normalized_dict1.keys()).difference(set(normalized_dict2.keys()))
            for key in missing_keys_in_dict2:
                mismatches.append((key, normalized_dict1[key], None))

            # Check for keys in normalized_dict2 that are missing in normalized_dict1
            missing_keys_in_dict1 = set(normalized_dict2.keys()).difference(set(normalized_dict1.keys()))
            for key in missing_keys_in_dict1:
                mismatches.append((key, None, normalized_dict2[key]))

            # Prepare output as a formatted string
            output = ""
            if mismatches:
                output += "Differences found:\n"
                for mismatch in mismatches:
                    if mismatch[1] is not None and mismatch[2] is not None:
                        output += f"Key '{mismatch[0]}' has different values: {mismatch[1]} (from Excel) vs {mismatch[2]} (from Application)\n"
                    elif mismatch[1] is not None:
                        output += f"Key '{mismatch[0]}' is present in Excel but missing in Application\n"
                    else:
                        output += f"Key '{mismatch[0]}' is present in Application but missing in Excel\n"
            else:
                output += "No differences found.\n"
            if matches:
                output += "\nMatching keys and values:\n"
                for match in matches:
                    output += f"Key '{match[0]}' has matching values: {match[1]}\n"
            # print(output)
            
    
    # Function to convert DataFrame columns and values into a dictionary
    def read_excel_to_dict(datafile):
        # Read the Excel file into a DataFrame
        
            df = pd.DataFrame(datafile)
            # Convert DataFrame to dictionary
            columns_values_dict = {}
        
            # Iterate over each column in the DataFrame
            for column in df.columns:
                # Convert column values to a list
                column_values = df[column].tolist()
                
                # Store the column and its corresponding values in the dictionary
                columns_values_dict[column] = column_values
    
            if columns_values_dict:
                # Output the dictionary containing columns and values
                print("Columns and Values from Excel:")
                for column, values in columns_values_dict.items():
                    print(f"{column}: {values}")
            else:
                print("Failed to read Excel file.")

            return columns_values_dict
    
    def compare_excel_to_webpage(excel_file, column_to_key_mapping,webpage_key_values):
        # Read Excel file
        df = pd.read_excel(excel_file)
        
        # Compare specified Excel columns with corresponding webpage key-value pairs
        for excel_column, webpage_key in column_to_key_mapping.items():
            if excel_column in df.columns and webpage_key in webpage_key_values:
                excel_values = df[excel_column].tolist()
                webpage_value = webpage_key_values[webpage_key]
                
                # Compare each value in the Excel column with the corresponding webpage value
                for value in excel_values:
                    if str(value) != webpage_value:
                        print(f"Mismatch found for column '{excel_column}': Excel value '{value}' does not match webpage value '{webpage_value}'")
                    else:
                        print(f"Keyvalue pairs are matching : '{excel_column}', '{webpage_value}','{value}' ")

    
    def normalize_key(key):
        """Normalize a key by removing spaces and converting to lowercase."""
        # return key.replace(' ', '').lower()
        return key.strip().replace(' ', '').lower()
    
            
# try:
#             # Find all <div> elements representing key-value pairs using XPath
#             #key_elements = self.base.findElements("Keyxpath")
#             key_elements=Key_xpath
#             ListofKeys=[]
#             ListofValues=[]
#             time.sleep(10)
#             #value_elements= self.base.findElements("Valuexpath")
#             value_elements=Value_Xpath
#             time.sleep(10)
#             # Iterate through key elements to extract key-value pairs 
#             LabelName_Key = [x.text for x in key_elements]
#             ListofKeys.append(LabelName_Key)
#             # print(LabelName_Key)
            
#             LabelName_Value = [x.text for x in value_elements]
#             ListofValues.append(LabelName_Value)
#             # Initialize a dictionary to store key-value pairs
#             # Add the key-value pair to the dictionary
#             key_value_pairs = dict(zip(LabelName_Key, LabelName_Value))
#             for key, value in zip(ListofKeys, ListofValues):
#                 key_value_pairs[key] = value

#             # Convert ListofValues to a single string
#             values_string = ', '.join(ListofValues)
#             # print(key_value_pairs)
            
#             print("\n Extracted Key-Value Pairs: \n", key_value_pairs)
#             print("\n Extracted Key-Value Pairs and converted as strings: \n",values_string)
#             return key_value_pairs

            
#         except Exception as e:
#             print(f"Error occurred while extracting key-value pairs: {e}")
#         */