import json
import re
import os

def concatenate_create_statements(sql):
    statements = []
    buffer = []
    for line in sql.splitlines():
        if not line or line.lower().startswith(r"\s*insert\s+into") or line.lower().startswith(r"\s*pragma"): continue
        if line.lower().startswith('#'): continue
        if line.lower().startswith('--'): continue
        line = line.strip()
        if not line:
            continue
        buffer.append(line)
        if line.endswith(';'):
            full_statement = ' '.join(buffer)
            statements.append(full_statement)
            buffer = []
    return statements

def parse_sql(sql):
    tables = []
    create_statements = concatenate_create_statements(sql)
    for statement in create_statements:
        # print(statement+'\n')
        if re.match(r'^\s*CREATE\s+TABLE', statement, re.IGNORECASE):
            current_table = parse_create_table(statement)
            # print(statement,current_table)
            parse_columns(statement, current_table)
            # print('done')
            tables.append(current_table)
    return {"tables": tables}

def parse_create_table(statement):
    match = re.match(r'^\s*CREATE\s+TABLE\s+(IF\s+NOT\s+EXISTS)?\s*[`"]?([^`"\s]+)[`"]?\s*\(', statement, re.IGNORECASE)
    if match:
        table_name = match.group(2)
        return {
            "name": table_name,
            "columns": [],
            "primary_key": [],
            "foreign_keys": [],
            "unique_constraints": []
        }
    else:
        raise ValueError(f"Invalid CREATE TABLE statement: {statement}")

def parse_columns(statement, current_table):
    columns_section = re.findall(r'\s*\(\s*(.*)\s*\)\s*\;', statement, re.DOTALL)[0]
    column_lines=[]
    to_push=""
    ptr=0
    for c in columns_section:
        if c==',' and ptr==0:
            column_lines.append(to_push)
            to_push=""
        else:
            if c=='(': ptr+=1
            elif c==')': ptr-=1
            to_push+=c            

    if to_push: column_lines.append(to_push)
    for line in column_lines:
        line = line.strip()
        reversed_line = line[::-1]
        if re.match(r'^\s*PRIMARY\s+KEY', line, re.IGNORECASE):
            parse_primary_key(line, current_table)
        elif re.match(r'^\s*YEK\s+YRAMIRP', reversed_line, re.IGNORECASE):
            parse_primary_key_end(line, current_table)
        elif re.match(r'^\s*FOREIGN\s+KEY', line, re.IGNORECASE):
            parse_foreign_key(line, current_table)
        elif re.match(r'\s*UNIQUE', line, re.IGNORECASE):
            parse_unique_constraint(line, current_table)
        elif re.match(r'\s*[`"]?[^`"\s]+[`"]?\s+[A-Za-z]', line):  # Column definition
            parse_column(line, current_table)

def parse_column(line, current_table):
    line.strip()
    # print(line)
    col_match = re.match(r'^\s*[`"]?([^`"\s]+)[`"]?\s+([^\$]+)', line, re.IGNORECASE)
    if col_match:
        column_name = col_match.group(1).strip(" `\"")
        column_type = col_match.group(2).strip(" `\"")
        current_table["columns"].append({
            "name": column_name.strip(),
            "type": column_type.strip()
        })
    else:
        raise ValueError(f"Invalid column definition: {line}")

def parse_primary_key(line, current_table):
    pk_match = re.findall(r'\s*PRIMARY\s+KEY\s*\([`"]?([^)]+)[`"]?\)', line, re.IGNORECASE)
    if pk_match:
        pk_columns = [quote_column_name(col.strip(" `\"")) for col in pk_match[0].split(',')]
        current_table["primary_key"] = pk_columns
    else:
        raise ValueError(f"Invalid PRIMARY KEY definition: {line}")

def parse_primary_key_end(line, current_table):
    # print('hi')
    col_match = re.match(r'^\s*[`"]?([^`"\s]+)[`"]?\s+([^\$]+)\s*PRIMARY\s+KEY\s*', line, re.IGNORECASE)
    if col_match:
        column_name = col_match.group(1).strip(" `\"")
        column_type = col_match.group(2).strip(" `\"")
        current_table["columns"].append({
            "name": column_name.strip(),
            "type": column_type.strip()
        })
        pk_list=[]
        pk_list.append(column_name)
        current_table["primary_key"] = pk_list
    else:
        raise ValueError(f"Invalid PRIMARY KEY definition: {line}")
    # pk_match = re.findall(r'\s*\([`"]?([^)]+)[`"]?\)\s+PRIMARY\s+KEY\s*', line, re.IGNORECASE)
    # if pk_match:
    #     pk_columns = [quote_column_name(col.strip(" `\"")) for col in pk_match[0].split(',')]
    #     current_table["primary_key"] = pk_columns
    # else:
    #     raise ValueError(f"Invalid PRIMARY KEY definition: {line}")

def parse_foreign_key(line, current_table):
    fk_match = re.findall(r'FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s*[`"]?([^`"]+)[`"]?\s*\(([^)]+)\)', line, re.IGNORECASE)
    if fk_match:
        fk_columns = [(col.strip(" `\"")) for col in fk_match[0][0].split(',')]
        fk_table = fk_match[0][1].strip(" `\"")
        fk_ref_columns = [(col.strip(" `\"")) for col in fk_match[0][2].split(',')]
        current_table["foreign_keys"].append({
            "columns": fk_columns,
            "table": fk_table,
            "ref_columns": fk_ref_columns
        })
    else:
        raise ValueError(f"Invalid FOREIGN KEY definition: {line}")

def parse_unique_constraint(line, current_table):
    uc_match = re.findall(r'UNIQUE\s*\(([^)]+)\)', line, re.IGNORECASE)
    if uc_match:
        uc_columns = [quote_column_name(col.strip(" `\"")) for col in uc_match[0].split(',')]
        current_table["unique_constraints"].append(uc_columns)
    else:
        raise ValueError(f"Invalid UNIQUE constraint definition: {line}")

def quote_column_name(column_name):
    return column_name

def generate_schema_json(sql_file_path, json_file_path):
    with open(sql_file_path, 'r') as sql_file:
        sql = sql_file.read()
    
    schema = parse_sql(sql)
    
    with open(json_file_path, 'w') as json_file:
        json.dump(schema, json_file, indent=4)

def process_all_databases(base_path):
    tot_db=0
    for root, dirs, files in os.walk(base_path):
        tot_db+=1
        for file in files:
            if file.endswith(".sql"):
                sql_file_path = os.path.join(root, file)
                json_file_path = os.path.splitext(sql_file_path)[0] + ".json"
                try:
                    generate_schema_json(sql_file_path, json_file_path)
                except Exception as e:
                    print(f"Failed to process {sql_file_path}: {e}")
    
    # print(tot_db)
# 
base_path = 'F:/OneDrive/Desktop/Study/NLP_ResearchProject/Project/spider/database'
process_all_databases(base_path)