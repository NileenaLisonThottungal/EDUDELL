import google.generativeai as genai
import streamlit as st
import pdfplumber

# Configure the API with your API key
genai.configure(api_key="AIzaSyDX3TwPWa5qX6MkJ6c2D3HlkCmx83KVrw0")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Function to summarize text
def summarize_text(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Please summarize the following text: \n\n{text}"])
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Function to answer a question based on text
def question_text(text, question):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Please answer the following question based on the provided text: \n\nText: {text} \n\nQuestion: {question}"])
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Function to generate multiple choice questions (MCQs)
def generate_mcqs(text, num_questions=1):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Please generate {num_questions} multiple-choice question(s) based on the following text: \n\n{text}"])
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Main function
def main():
    st.set_page_config(page_title="AI-Powered PDF Assistant", page_icon="📄", layout="centered")
    st.title("📄 AI-Powered PDF Assistant")

    # Introduction
    st.markdown(
        """
        <style>
            .intro {font-size: 1.2em; color: #4CAF50;}
        </style>
        """, unsafe_allow_html=True
    )
    st.markdown('<p class="intro">Upload a PDF file to summarize, answer questions, or generate multiple-choice questions.</p>', unsafe_allow_html=True)

    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload your PDF here:", type="pdf")

    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        display_text = text[:500] + ('...' if len(text) > 500 else '')

        # Display extracted text with expandable section
        st.subheader("Extracted Text")
        with st.expander("View Extracted Text"):
            st.write(display_text)

        # Divider line
        st.write("---")

        # Summary Section
        st.subheader("Generate Summary")
        if st.button("🔍 Get Summary"):
            summary = summarize_text(text)
            st.success("Summary Generated:")
            st.write(summary)

        # Divider line
        st.write("---")

        # Question Answering Section
        st.subheader("Ask a Question")
        question = st.text_input("Enter your question about the text")
        if st.button("🤔 Get Answer"):
            if question:
                answer = question_text(text, question)
                st.success("Answer Generated:")
                st.write(answer)
            else:
                st.warning("Please enter a question to get an answer.")

        # Divider line
        st.write("---")

        # MCQ Generation Section with option to specify number of questions
        st.subheader("Generate MCQs")
        num_questions = st.number_input("Number of MCQs to generate", min_value=1, max_value=10, value=1)
        if st.button("📝 Generate MCQ"):
            mcq = generate_mcqs(text, num_questions)
            st.success(f"{num_questions} MCQ(s) Generated:")
            st.write(mcq)

    else:
        st.info("Please upload a PDF file to start.")

if __name__ == "__main__":
    main()
