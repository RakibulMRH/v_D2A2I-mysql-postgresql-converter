import sys
import os
import re
import getpass
import subprocess
import json

def convert_insert_statements(mysql_statements):
    psql_statements = []
    for i, statement in enumerate(mysql_statements):
        # Replace '0000-00-00 00:00:00' and '0000-00-00' with '1970-01-01 00:00:00' and '1970-01-01' respectively
        statement = statement.replace("'0000-00-00 00:00:00'", "'1970-01-01 00:00:00'")
        statement = statement.replace("'0000-00-00'", "'1970-01-01'")
        statement = statement.replace("Cox\\'s", "Coxs")  # Escape the backslash
        statement = statement.replace("Cox's", "Coxs")
        statement = statement.replace("\\'C", "C")  # Replace escaped single quote with double single quotes
        

        # Replace escaped characters with E escape string syntax
        statement = statement.replace("\\r", "")
        statement = statement.replace("\\n", " ")  # Replace newline with space
        statement = statement.replace("\'C'", "C")  # Replace escaped double quotes with single quotes
        statement = statement.replace("\\", "")  # Replace escaped single quotes with single quotes
        # statement = statement.replace('\"', "")  # Replace escaped single quotes with double single quotes

        # Handle single quotes within string literals
        # statement = re.sub(r"'(.*?)'", lambda m: m.group(0).replace("'", "''"), statement)
        #statement = re.sub(r"(\{.*?\})", lambda m: json.dumps(json.loads(m.group(1))), statement)

        # Handle curly braces within string literals
        statement = re.sub(r"'{(.*?)}'", lambda m: m.group(0).replace('"{', "'{").replace('}"', "}'"), statement) 
        mysql_statements[i] = statement  # Update the statement in the list
 
        # Convert `ON DUPLICATE KEY UPDATE` to `ON CONFLICT DO UPDATE`
        if 'ON DUPLICATE KEY UPDATE' in statement:
            match = re.search(r'INSERT INTO (\w+) \((.*?)\) VALUES \((.*?)\) ON DUPLICATE KEY UPDATE (.*?);', statement, re.IGNORECASE)
            if match:
                table = match.group(1)
                columns = match.group(2)
                values = match.group(3)
                updates = match.group(4)
                
                # Prepare the conflict target and update clause
                conflict_target = columns.split(',')[0].strip()  # Assume the first column is the primary key
                update_clause = ', '.join([f"{col.split('=')[0].strip()} = EXCLUDED.{col.split('=')[0].strip()}" for col in updates.split(',')])
                
                psql_statement = f"INSERT INTO {table} ({columns}) VALUES ({values}) ON CONFLICT ({conflict_target}) DO UPDATE SET {update_clause};"
                psql_statements.append(psql_statement)
        else:
            # Directly use the statement as PostgreSQL-compatible
            psql_statements.append(statement)
    
    return psql_statements

def write_to_file(filename, statements, max_size_mb=500):
    file_index = 0
    current_file = f"{filename}"
    current_size = 0
    with open(current_file, 'w') as outfile:
        for statement in statements:
            statement_size = len(statement.encode('utf-8'))
            if current_size + statement_size > max_size_mb * 1024 * 1024:
                file_index += 1
                current_file = f"{filename}_{file_index}"
                outfile = open(current_file, 'w')
                current_size = 0
            outfile.write(statement + '\n')
            current_size += statement_size

def main():
    if len(sys.argv) != 3:
        print("Usage: python db_converter.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    base_output_file = os.path.splitext(output_file)[0] + ".plsql"
    
    # Read MySQL statements from the input file
    with open(input_file, 'r') as infile:
        mysql_statements = infile.readlines()
    
    # Convert MySQL statements to PostgreSQL format
    psql_statements = convert_insert_statements(mysql_statements)
    
    # Write PostgreSQL statements to the output files, splitting if larger than 500MB
    write_to_file(base_output_file, psql_statements)
    
    print(f"Converted SQL statements have been written to {base_output_file} (and possibly additional split files)")

if __name__ == "__main__":
    main()
