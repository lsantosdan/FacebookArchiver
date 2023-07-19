import os
import shutil
import json

def copy_json_content(directory):
    json_count = 0
    with open('./json.txt', 'w') as output_file:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    print(f"Processing JSON file: {file_path}")
                    with open(file_path, 'r') as json_file:
                        try:
                            json_data = json.load(json_file)
                            json.dump(json_data, output_file)
                            output_file.write('\n')  # Add a newline after each JSON object
                            json_count += 1
                        except json.JSONDecodeError:
                            print(f"Failed to read JSON file: {file_path}")
    print(f"Total JSON files processed: {json_count}")

# Specify the directory to start from
starting_directory = './'
copy_json_content(starting_directory)