import csv
import datetime

def search_json(filepath):
    # Read the json.txt file
    with open("json.txt", "r", encoding="utf-8") as file:
        json_data = file.read()

    # Step 2: If the filepath starts with "messages/"
    if filepath.startswith("messages/"):
        # Find the location of the filepath in json.txt
        file_location = json_data.find(filepath)
        
        # Calculate the end of filepath
        end_of_filepath = file_location + len(filepath)
        
        # Reverse search for the first occurrence of "timestamp_ms" from file_location
        raw_metadata = json_data[:file_location][::-1].find("sm_pmatsemit") + 13 + len(filepath)
        
        # Store the substring starting from "timestamp_ms" to file_location
        raw_metadata = json_data[end_of_filepath - raw_metadata:end_of_filepath]

    # Step 3: If the filepath does not start with "messages/"
    else:
        # Find the location of the filepath in json.txt
        file_location = json_data.find(filepath)

        # Search for the next occurrence of '{"uri":"' from file_location
        end_of_metadata = json_data.find("{\"uri\":", file_location)

        # If end_of_metadata is not found, use the end of json_data
        if end_of_metadata == -1:
            end_of_metadata = len(json_data)

        # Store the substring starting from the beginning of file_location to end_of_metadata
        raw_metadata = json_data[file_location:end_of_metadata]

    # Step 4: Extract timestamps from raw_metadata
    timestamps = ["taken_timestamp", "creation_timestamp", "timestamp_ms"]
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for tag in timestamps:
        if tag in raw_metadata:
            start_index = raw_metadata.find(tag) + len(tag) + 3
            end_index = raw_metadata.find(",", start_index)
            if end_index == -1:
                end_index = raw_metadata.find("}", start_index)
            timestamp = raw_metadata[start_index:end_index].strip().replace("\"", "")
            break

    # Step 6: Convert timestamp to European Central Time (CET)
    if timestamp != "Timestamp not found":
        if "timestamp_ms" in raw_metadata:
            timestamp = timestamp[:10]  # Round down to 10 characters for timestamp_ms
        timestamp = int("".join(filter(str.isdigit, timestamp)))  # Extract only numeric characters

        try:
            timestamp = datetime.datetime.fromtimestamp(timestamp)
            cest = datetime.timezone(datetime.timedelta(hours=2))
            timestamp = timestamp.astimezone(cest).strftime("%Y-%m-%d %H:%M:%S")
        except OSError:
            # Set the timestamp to the current date and time
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Step 6: Extract description from raw_metadata
    description = ""
    if "\"description\":" in raw_metadata:
        start_index = raw_metadata.find("\"description\":") + len("\"description\":") + 2
        end_index = raw_metadata.find("}", start_index) -1
        if end_index != -1:
            description = raw_metadata[start_index:end_index]

    return timestamp, description


# Open the CSV file
with open("photosvideos.csv", "r", encoding="utf-8") as csv_file:
    # Create a CSV reader
    reader = csv.reader(csv_file)
    # Read the header row
    header = next(reader)
    # Add "timestamp" and "description" to the header
    header.extend(["timestamp", "description"])
    # Create a list to store the modified rows
    modified_rows = [header]
    
    # Process each row in the CSV file
    for row in reader:
        # Get the filepath from the row
        filepath = row[0]

        # Call the search_json function to retrieve timestamp and description
        timestamp, description = search_json(filepath)

        # Append the retrieved values to the row
        row.extend([timestamp, description])

        # Append the modified row to the list
        modified_rows.append(row)

        # Print a success message for each processed filepath
        print("Processed file:", filepath)

# Write the modified rows to a new CSV file
with open("photosvideos_metadata.csv", "w", encoding="utf-8-sig", newline="") as output_file:
    # Create a CSV writer
    writer = csv.writer(output_file)
    # Write the modified rows
    writer.writerows(modified_rows)