# Define the input and output file paths
input_file_path = 'app.log'
output_file_path = 'extracted_data.txt'

# Open the input log file and the output file
with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
    for line in infile:
        # Split the line into parts
        parts = line.split(" - DEBUG - Received user message: ")

        # Extract the timestamp and message
        if len(parts) == 2:
            timestamp = parts[0].strip()
            user_message = parts[1].strip()

            # Write the results to the output file
            outfile.write(f"Timestamp: {timestamp}\n")
            outfile.write(f"User Message: {user_message}\n")
            outfile.write("\n")
