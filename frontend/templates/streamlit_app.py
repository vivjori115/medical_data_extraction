import streamlit as st
import requests

# FastAPI server URL
API_URL = "http://127.0.0.1:8000/extract_from_doc"

def upload_file():
    st.title("Document Extraction Tool")
    st.write("Upload a PDF document to extract prescription or patient details.")
    
    file_format = st.selectbox("Select Document Format", ("prescription", "patient_details"))
    file = st.file_uploader("Choose a file", type="pdf")
    
    if file:
        # Display a preview of the uploaded file (optional)
        st.write(f"File: {file.name}")
        
        # Show a button to submit the file
        if st.button("Extract Data"):
            try:
                # Prepare the file and send it to FastAPI
                files = {'file': file.getvalue()}
                data = {'file_format': file_format}
                response = requests.post(API_URL, data=data, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.write("Extracted Data:")
                    st.json(result)
                else:
                    st.error("Error occurred while extracting data.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    upload_file()
