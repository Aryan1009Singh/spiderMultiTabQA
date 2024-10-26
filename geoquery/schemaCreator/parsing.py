import json
import re
import os

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct absolute paths to the files
SQLpath = os.path.join(script_dir, "../../../GEOQUERY/geo_mysql_dump.db")

def parse_sql_schema(sql):
    table_name = None
    columns = []
    keys = []
    primary_key = None

    # Regex patterns to match table name, columns, keys, and primary key
    table_pattern = re.compile(r'CREATE TABLE `(\w+)`')
    column_pattern = re.compile(r'`(\w+)` (\w+\(?\d*\)?) (NOT NULL|DEFAULT NULL|DEFAULT \'\d+\')?')
    key_pattern = re.compile(r'KEY `(\w+)` \(`(\w+)`\(?\d*\)?\)')
    primary_key_pattern = re.compile(r'PRIMARY KEY \(`(\w+)`\)')

    for line in sql.splitlines():
        table_match = table_pattern.search(line)
        if table_match:
            table_name = table_match.group(1)
            continue

        column_match = column_pattern.search(line)
        if column_match:
            column_name = column_match.group(1)
            column_type = column_match.group(2)
            column_constraints = column_match.group(3)
            columns.append({
                "name": column_name,
                "type": column_type,
                "constraints": column_constraints
            })
            continue

        key_match = key_pattern.search(line)
        if key_match:
            key_name = key_match.group(1)
            key_column = key_match.group(2)
            keys.append({
                "name": key_name,
                "column": key_column
            })
            continue

        primary_key_match = primary_key_pattern.search(line)
        if primary_key_match:
            primary_key = primary_key_match.group(1)

    if table_name:
        return {
            table_name: {
                "columns": columns,
                "keys": keys,
                "primary_key": primary_key
            }
        }
    return {}

def save_schema_to_json(schema, filename):
    with open(filename, 'w') as json_file:
        json.dump(schema, json_file, indent=4)

# Read the SQL file
with open(SQLpath, 'r') as file:
    sql_content = file.read()

# Split the SQL content into individual table definitions
table_definitions = sql_content.split('CREATE TABLE')

# Initialize an empty dictionary to hold the combined schema
combined_schema = {}

# Parse each table definition and combine the results
for table_definition in table_definitions:
    if table_definition.strip():  # Skip empty strings
        parsed_schema = parse_sql_schema('CREATE TABLE' + table_definition)
        combined_schema.update(parsed_schema)

# Save the combined schema to a JSON file
save_schema_to_json(combined_schema, 'F:/OneDrive/Desktop/Study/NLP_ResearchProject/Project/geoquery/schemaCreator/combined_schema.json')

print("Combined schema saved to combined_schema.json")