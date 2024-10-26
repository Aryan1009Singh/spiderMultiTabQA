import os
import json

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths to the files
devSQL_path = os.path.join(script_dir, "../../../ATIS/dev.sql")
testSQL_path = os.path.join(script_dir, "../../../ATIS/test.sql")
train_devSQL_path = os.path.join(script_dir, "../../../ATIS/train_dev.sql")
trainSQL_path = os.path.join(script_dir, "../../../ATIS/train.sql")

testNL_path = os.path.join(script_dir, "../../../ATIS/test.nl")
devNL_path = os.path.join(script_dir, "../../../ATIS/dev.nl")
train_devNL_path = os.path.join(script_dir, "../../../ATIS/train_dev.nl")
trainNL_path = os.path.join(script_dir, "../../../ATIS/train.nl")

# Read the files
with open(devSQL_path, "r") as f:
    devSQL = f.readlines()

with open(testSQL_path, "r") as f:
    testSQL = f.readlines()

with open(train_devSQL_path, "r") as f:
    train_devSQL = f.readlines()

with open(trainSQL_path, "r") as f:
    trainSQL = f.readlines()

with open(devNL_path, "r") as f:
    devNL = f.readlines()

with open(testNL_path, "r") as f:
    testNL = f.readlines()

with open(train_devNL_path, "r") as f:
    train_devNL = f.readlines()

with open(trainNL_path, "r") as f:
    trainNL = f.readlines()

# Initialize dictionaries
combined = {}

def extract_table_names(sql_query, table_list):
    # Convert the SQL query to lowercase
    sql_query_lower = sql_query.lower()

    # Extract table names using map and filter, and store them in a set to avoid duplicates
    extracted_tables_set = set(filter(lambda table: table in sql_query_lower, map(str.lower, table_list)))

    # Convert the set back to a list to maintain the order and return it
    extracted_tables_list = list(extracted_tables_set)

    return extracted_tables_list

table_list = ["aircraft", "airline", "airport", "airport_service", "city", "class_of_service", "code_description", "compartment_class", "date_day", "days", "dual_carrier", "equipment_sequence", "fare", "fare_basis", "flight", "flight_fare", "flight_leg", "flight_stop", "food_service", "ground_service", "month", "restriction", "state", "time_interval", "time_zone"]

# Create data
def createData():
    j = 0
    for i in range(len(devSQL)):
        tables = extract_table_names(devSQL[i], table_list)
        combined[j] = {
            "question": devNL[i].strip(),
            "query": devSQL[i].strip(),
            "tables": tables
        }
        j += 1
    for i in range(len(testSQL)):
        tables = extract_table_names(testSQL[i], table_list)
        combined[j] = {
            "question": testNL[i].strip(),
            "query": testSQL[i].strip(),
            "tables": tables
        }
        j += 1
    for i in range(len(train_devSQL)):
        tables = extract_table_names(train_devSQL[i], table_list)
        combined[j] = {
            "question": train_devNL[i].strip(),
            "query": train_devSQL[i].strip(),
            "tables": tables
        }
        j += 1
    for i in range(len(trainSQL)):
        tables = extract_table_names(trainSQL[i], table_list)
        combined[j] = {
            "question": trainNL[i].strip(),
            "query": trainSQL[i].strip(),
            "tables": tables
        }
        j += 1

createData()

saving_path = os.path.join(script_dir, "../../../ATIS/combined.json")

print(len(combined))

with open(saving_path, "w") as json_file:
    json.dump(combined, json_file, indent=4)

print("Data saved")

