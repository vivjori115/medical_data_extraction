from flask import Flask, request, jsonify
import uuid
import os
from extractor import extract

app = Flask(__name__)

@app.route('/extract_from_doc', methods=['POST'])
def extract_from_doc():
    # Extract file format and file from the form data
    file_format = request.form.get('file_format')
    file = request.files.get('file')

    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    if not file_format:
        return jsonify({'error': 'File format not provided'}), 400

    # Save the uploaded file to a temporary location
    file_path = "../uploads/" + str(uuid.uuid4()) + ".pdf"
    file.save(file_path)

    try:
        # Extract data from the file using the provided extractor function
        data = extract(file_path, file_format)
    except Exception as e:
        data = {'error': str(e)}

    # Delete the uploaded file after processing
    if os.path.exists(file_path):
        os.remove(file_path)

    # Return the extracted data (or error)
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
