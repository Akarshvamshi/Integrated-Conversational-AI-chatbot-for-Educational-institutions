from flask import Flask, request, jsonify, send_from_directory, render_template
import requests
import logging
import re

app = Flask(__name__)
input_file_path = 'app.log'
output_file_path = 'extracted_data.txt'
logging.basicConfig(
    filename='app.log',  # Log file name
    filemode='a',  # Append mode
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Log level
)
logger = logging.getLogger(__name__)

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"


@app.route('/')
def index():
    return send_from_directory('', 'templates/index.html')


@app.route('/about')
def about():
    return send_from_directory('', 'templates/about.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    response = requests.post(RASA_URL, json={"message": user_message})

    logger.debug(f"Received user message: {user_message}")

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to get a valid response"}), response.status_code


def extract_data(input_file_path, output_file_path):
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


if __name__ == '__main__':
    app.run(port=5000)
    extract_data(input_file_path, output_file_path)
