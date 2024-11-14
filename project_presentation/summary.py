import os
import streamlit as st
from transformers import pipeline
from io import BytesIO
from pdfplumber import open as open_pdf
from docx import Document
import base64

# Suppress TensorFlow warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Initialize the summarization pipeline
summarization_pipeline = pipeline("summarization", model="google/pegasus-xsum")

# Helper function to decode document content based on file type
def parse_document_content(file):
    # Detect file type from file name
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        return parse_pdf(file)
    elif file.name.endswith(".docx"):
        return parse_docx(file)
    else:
        return "Unsupported file type. Please upload a .txt, .pdf, or .docx file."

# PDF parsing function
def parse_pdf(file):
    text = ""
    with open_pdf(file) as pdf:
        # Extract text from each page in parallel
        for page in pdf.pages:
            text += page.extract_text()
    return text

# DOCX parsing function
def parse_docx(file):
    document = Document(file)
    text = "\n".join([para.text for para in document.paragraphs])
    return text

# Function to split and summarize large documents with optimized max_length
def summarize_large_document(document_text):
    max_chunk_length = 500  # Adjust based on model's token limit
    chunks = [document_text[i:i+max_chunk_length] for i in range(0, len(document_text), max_chunk_length)]
    summary = ""
    for chunk in chunks:
        chunk_length = len(chunk.split())
        adjusted_max_length = min(130, int(chunk_length * 0.5))  # set max_length to roughly half the chunk length
        partial_summary = summarization_pipeline(
            chunk,
            max_length=adjusted_max_length,
            min_length=30,
            do_sample=False
        )[0]["summary_text"]
        summary += partial_summary + " "
    return summary

# Streamlit app layout
st.title("Document Summarization App")

uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    document_text = parse_document_content(uploaded_file)
    if document_text.startswith("Unsupported"):
        st.error(document_text)
    else:
        summary = summarize_large_document(document_text)
        st.subheader("Document Summary")
        st.write(summary)
