import csv
import os
import shutil

input_file = "photosvideos_metadata.csv"
temp_file = "photosvideos_metadata_temp.csv"

# Create a temporary file to write the modified rows
shutil.copyfile(input_file, temp_file)

# Modify the rows in the temporary file
with open(temp_file, "r", encoding="utf-8-sig") as file:
    reader = csv.reader(file)
    rows = list(reader)

# Update the header row with the new column name
header_row = rows[0]
header_row.insert(1, "filename")

for row in rows[1:]:
    first_column_value = row[0]
    last_slash_index = first_column_value.rfind("/")
    filename = first_column_value[last_slash_index + 1:]
    row.insert(1, filename)

# Overwrite the input file with the modified rows
with open(input_file, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(rows)

# Remove the temporary file
os.remove(temp_file)

print(f"CSV file '{input_file}' has been updated.")

