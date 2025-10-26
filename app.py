# app.py (Colorful Dashboard Design)
import streamlit as st
import pandas as pd
import os
import json
from io import BytesIO

# Assuming your original parser.py and text_extractor.py files are present
from text_extractor import extract_text 
from parser import parse_resume 

# --- Custom CSS for Colorful, Modern Look ---
def set_custom_styles():
    st.markdown("""
        <style>
        /* General Body and Font */
        .stApp {
            background-color: #ffffff; /* White background */
            color: #333333;
        }
        /* Hide Streamlit default footer and menu */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom Title Header Styling */
        .title-container h1 {
            color: #4CAF50; /* Green color for the main title */
            font-weight: 800;
            text-align: center;
            padding-bottom: 10px;
        }
        
        /* Custom styling for st.metric cards (Key Info) */
        [data-testid="stMetric"] {
            background-color: #f7f7f7; /* Light background for metric cards */
            border-radius: 10px;
            padding: 15px 10px 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            border-left: 5px solid #007bff; /* Blue accent line */
        }
        
        /* Section Header Styles */
        h2 {
            color: #007bff; /* Blue color for section headers */
            border-bottom: 2px solid #007bff;
            padding-bottom: 5px;
            margin-top: 20px;
        }
        
        /* Button Styling */
        .stButton>button {
            border-radius: 20px;
            border: 1px solid #4CAF50;
            color: white;
            background-color: #4CAF50;
            padding: 10px 20px;
            transition: all 0.2s;
        }
        .stButton>button:hover {
            background-color: #388E3C; /* Darker green on hover */
            border-color: #388E3C;
        }
        
        /* Styling the Expander for Raw Text */
        [data-testid="stExpander"] {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 5px;
        }
        </style>
        """, unsafe_allow_html=True)

# --- Streamlit UI Setup ---
set_custom_styles()
st.set_page_config(page_title="Smart Resume Parser", layout="wide")

# Custom Title Header
st.markdown('<div class="title-container"><h1>📄 Smart Resume Parser</h1></div>', unsafe_allow_html=True)
st.markdown("---")

# File Uploader Section in the sidebar for a cleaner main layout
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=['pdf', 'docx'], help="Max 200MB file size.")

# Main Application Logic
if uploaded_file is not None:
    st.balloons() 

    # 1. & 2. Save, Extract Text
    file_extension = uploaded_file.name.split('.')[-1]
    temp_file_path = f"temp_resume.{file_extension}"

    file_bytes = uploaded_file.read()
    with open(temp_file_path, "wb") as f:
        f.write(file_bytes)

    with st.spinner("Processing file..."):
        resume_text = extract_text(temp_file_path, file_extension)

    st.markdown("## Extracted Information")

    if not resume_text.startswith("Error"):
        # 3. Parse Resume
        parsed_info = parse_resume(resume_text)
            
        # --- 1. CORE INFO DISPLAY (Using st.metric for a card look) ---
        col1, col2, col3 = st.columns(3)
        
        # Display Name
        col1.metric("Candidate Name", parsed_info.get('Name', 'N/A'))
        
        # Display Email
        col2.metric("Email Address", parsed_info.get('Email', 'N/A'))
        
        # Display Phone
        col3.metric("Phone Number", parsed_info.get('Phone', 'N/A'))

        st.markdown("---")
        
        # --- 2. SKILLS AND SNIPPET ---
        
        # Skills Display (Using a colorful markdown badge style)
        st.subheader("Skills Found")
        
        skills = parsed_info.get('Skills', 'N/A').split(', ')
        skill_html = ""
        for skill in skills:
            if skill and skill != 'N/A':
                # Custom CSS for a rounded badge
                skill_html += f'<span style="background-color: #4CAF50; color: white; padding: 5px 10px; margin: 3px; border-radius: 15px; display: inline-block; font-size: 0.9em;">{skill.strip()}</span>'
        
        st.markdown(skill_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # --- 3. EXPORT AND RAW TEXT ---
        st.subheader("Data Export & Debugging")
        
        df_export = pd.DataFrame([parsed_info])
        col_json, col_csv, col_raw = st.columns([1, 1, 2])

        # JSON Export
        json_data = json.dumps(parsed_info, indent=4)
        col_json.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"{uploaded_file.name.split('.')[0]}_parsed.json",
            mime="application/json"
        )

        # CSV Export
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        col_csv.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"{uploaded_file.name.split('.')[0]}_parsed.csv",
            mime="text/csv"
        )

        with col_raw.expander("Review Raw Text Snippet (First 500 characters)"):
            st.code(parsed_info.get('Raw Text (Snippet)', 'N/A'), language='text')

    else:
        st.error(f"Failed to process file: {resume_text}")

    # Clean up the temporary file
    try:
        os.remove(temp_file_path)
    except OSError:
        pass
        
else:
    # Instructions/Welcome screen when no file is uploaded
    st.info("⬆️ Please upload a PDF or DOCX file using the sidebar on the left to begin parsing.")
    st.markdown("""
    ### Project Deliverables Summary:
    * **Core Extraction:** Name, Email, Phone, Skills.
    * **Output Formats:** CSV and JSON export options.
    * **Technologies:** Python, Streamlit (UI), PyMuPDF/docx (File I/O), spaCy/Regex (NLP).
    """)