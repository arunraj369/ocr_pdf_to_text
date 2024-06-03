import re
from pymongo import MongoClient, errors
from PyPDF2 import PdfReader

def parse_resume_text(text):
    print(text)
    name_pattern = r'Name:\s*(.+)'
    role_pattern = r'Role:\s*(.+)'
    education_pattern = r'Education:\s*(.+)'
    location_pattern = r'Location:\s*(.+)'
    experience_pattern = r'Experience:\s*(.+)'

    name_match = re.search(name_pattern, text, re.IGNORECASE)
    role_match = re.search(role_pattern, text, re.IGNORECASE)
    education_match = re.search(education_pattern, text, re.IGNORECASE)
    location_match = re.search(location_pattern, text, re.IGNORECASE)
    experience_match = re.search(experience_pattern, text, re.IGNORECASE)

    name = name_match.group(1) if name_match else None
    role = role_match.group(1) if role_match else None
    education = education_match.group(1) if education_match else None
    location = location_match.group(1) if location_match else None
    experience = experience_match.group(1) if experience_match else None

    return {'Name': name, 'Role': role, 'Education': education, 'Location': location, 'Experience': experience}

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_object:
            reader = PdfReader(pdf_object)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text

def main():
    # Connect to MongoDB
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['resume_database']
        collection = db['resumes']
    except errors.ConnectionError as e:
        print(f"Error connecting to MongoDB: {e}")
        return

    # Path to the PDF file
    pdf_path = 'D:\\Resume\\folder\\aee.pdf'

    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("No text extracted from the PDF.")
        return

    # Parse the text and extract information
    resume_info = parse_resume_text(text)
    if resume_info:
        collection.insert_one(resume_info)
        print("Resume information successfully inserted into MongoDB:")
        print(resume_info)
    else:
        print("No resume information found in the extracted text.")

if __name__ == "__main__":
    main()


# I seperate text from pdf with py2pdf and tessereact i used py2pdf in this code
# Text seperation and storing data in  MongoDb are successfully Done
# I tried regex method for matching word what we want match and also I tried spacy library to match the keywords both get failure
# this my proces
# while i check with online NLP methode is more efficient by using openai API to find matching words and it like chatbot. 
# Now i Plan to try with NLP methode match those word 