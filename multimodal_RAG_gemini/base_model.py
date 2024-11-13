import google.generativeai as genai
import streamlit as st
# from google.cloud import aiplatform
import os
import pdfplumber
from langchain_community.document_loaders import PyPDFLoader

genai.configure(api_key="AIzaSyDX3TwPWa5qX6MkJ6c2D3HlkCmx83KVrw0")



def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text 



def summarize_text(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Please summarize the following text: \n\n{text}"])
        return response.text
    except Exception as e:
        return f"An error occured: {e}"

def question_text(text,question):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Please answer the following question based on the provided text: \n\nText: {text} \n\nQuestion: {question}"])
        return response.text 
    except Exception as e:
        return f"An error occured: {e}"
    
def main():
    st.title("PDF Summarizer and Question answering with Gemini")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        display_text = text[:500] + ('...' if len(text)>500 else '')

        st.subheader("Extracted text")
        st.text_area("Text from PDF",display_text, height=300)

        if st.button("Get Summary"):
            summary = summarize_text(text)
            st.subheader("Summary")
            st.write(summary)

        question = st.text_input("Enter your question about the text")
        if st.button("Get Answer"):
            if question:
                answer = question_text(text, question)
                st.subheader("Answer")
                st.write(answer)
            else:
                st.write("Please enter a question to get an answer")

if __name__ == "__main__":
    main()
