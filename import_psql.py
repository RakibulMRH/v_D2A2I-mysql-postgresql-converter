import os
import subprocess
import getpass

# Directory containing the .psql files
directory = "E:\\AIUB\\DA2I2 Internship\\Resources\\"

# Get the password
password = getpass.getpass("Enter your password: ")

# Get the file name to import (without extension) from the user
file_name_to_import = input("Enter the name of the file to import (without extension): ")

# Sort the files in the directory
files = sorted(os.listdir(directory))

# Iterate over all files in the directory
for index, filename in enumerate(files):
    # Get the file name without extension
    name_without_ext = os.path.splitext(filename)[0]
    # Check if the file name is the one to import
    if name_without_ext == file_name_to_import:
        # Construct the full file path
        filepath = os.path.join(directory, filename)
        # Construct the psql command
        command = f'"C:\\Program Files\\PostgreSQL\\16\\bin\\psql" -h localhost -d trp-app -U postgres -f "{filepath}"'
        # Set the PGPASSWORD environment variable
        os.environ['PGPASSWORD'] = password
        # Execute the command
        subprocess.run(command, shell=True, check=True)