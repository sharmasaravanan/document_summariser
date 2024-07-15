import streamlit as st
import docx2txt
import os
import re
import string


# Create a directory to store uploaded files
def save_uploaded_file(uploaded_file):
    # Create a directory to store uploaded files
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    # Save the file
    with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())  # Save the file in 'uploads' directory
    return os.path.join("uploads", uploaded_file.name)


# Process the uploaded file
def process_uploaded_file(uploaded_file):
    # Process the file based on file type
    content = ""
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Handle .docx file
        content = docx2txt.process(uploaded_file)
    elif uploaded_file.type == "text/plain":
        # Handle .txt file
        content = uploaded_file.read().decode("utf-8")
    return content


# Main function
def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = " ".join(text.split())
    # Remove punctuation (except periods)
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    # Remove special characters and digits
    text = re.sub(r"[^a-zA-Z\s.]", "", text)
    return text


def main():
    st.title('Document Summarizer App')
    st.write('Upload a text file or enter text to analyze.')

    # Upload file or input text
    uploaded_file = st.file_uploader("Choose a file", type=['txt', 'docx'])
    text_input = st.text_area("Or enter text manually")

    if uploaded_file is not None:
        # Process uploaded file
        file_path = save_uploaded_file(uploaded_file)
        content = process_uploaded_file(uploaded_file)
    elif text_input:
        # Use manually entered text
        content = text_input.strip()
    else:
        st.warning('Please upload a file or enter text.')

    # Display the content
    if 'content' in locals():
        st.subheader('Original Content')
        st.text_area("", value=content, height=400)

        # Clean the content
        cleaned_content = clean_text(content)
        st.subheader('Preprocessed Content')
        st.text_area("", value=cleaned_content, height=400)

        st.subheader('Summary')
        # summary = summarize_text(cleaned_content)
        word_count = len(content.split())
        st.write(f"Word count: {word_count}")

        # You can add more analysis or processing here


if __name__ == "__main__":
    main()
