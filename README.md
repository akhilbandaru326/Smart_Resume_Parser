Smart Resume Parser
Project Overview
This project is a powerful, Python-based application designed to automate the extraction of structured information from unstructured resume documents. It addresses the common recruitment challenge of manually processing files like PDFs and DOCX by quickly converting them into clean, machine-readable data. The core goal is to accelerate the data intake process, making it simple to manage candidate details, technical skills, and work history.

Key Features & Technologies
The Smart Resume Parser is built using a modern stack focused on document processing and Natural Language Processing (NLP). The application is deployed via a clean, colorful web interface built with Streamlit, providing an immediate, professional user experience. Key information, such as Name, Email, Phone, and Skills, is presented in an easy-to-read dashboard format. Under the hood, the system uses PyMuPDF and python-docx for reliable text extraction, and a custom pipeline leveraging spaCy and Regular Expressions (Regex) for targeted data extraction. The output is directly downloadable as CSV and JSON files for seamless integration into databases or Applicant Tracking Systems (ATS).

Getting Started
Prerequisites
You need Python 3.x installed. We highly recommend using a virtual environment (venv).

Installation
Clone the repository:

Bash

git clone https://github.com/akhilbandaru326/smart-resume-parser.git
cd smart-resume-parser
Create and activate the virtual environment:

Bash

python -m venv venv
# For Windows PowerShell:
.\venv\Scripts\Activate.ps1
# For macOS/Linux Bash:
# source venv/bin/activate
Install dependencies:

Bash

pip install streamlit PyMuPDF python-docx spacy pandas
python -m spacy download en_core_web_sm
How to Run
Execute the following command in your activated terminal:

Bash

streamlit run app.py
The application will launch in your web browser. Use the file upload widget to submit a PDF or DOCX resume and instantly view the extracted, structured data.

Project Structure
The codebase is organized into three main modules:

app.py: The Streamlit application interface and main execution file.

text_extractor.py: Contains functions to handle file I/O and convert PDF/DOCX content into raw text.

parser.py: Houses the core NLP logic, including text cleaning, spaCy for Named Entity Recognition, and Regex for pattern matching and skill extraction.

Future Scope
While the current parser is highly effective, future enhancements could focus on Machine Learning integration. This includes training custom classification models to accurately delineate unstructured sections like Education and Experience, and exploring Optical Character Recognition (OCR) integration to handle scanned image-based resumes.
