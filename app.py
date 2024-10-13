import streamlit as st
import os
from llm import llm
import tempfile
from rag import create_qa_pipeline, load_pdf

# Set Streamlit app configuration
st.set_page_config(page_title="PDF-ingestion-QnA-system", page_icon="📰")

# Streamlit App title and sidebar
st.title("PDF QnA App")
st.sidebar.header("PDF QnA App")
st.sidebar.markdown("This app allows you to ask questions about your PDF files.")
st.sidebar.header("Upload PDF files")

# Initialize vectorstore in session state if it doesn't exist
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None

# Upload PDF files
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

# Proceed button after the file is uploaded
if uploaded_file:
    if st.sidebar.button("Proceed"):
        with st.spinner("Processing... Please wait."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.read())  # Write the uploaded file's contents to the temp file
                    temp_file_path = temp_file.name
                
                # Load the PDF and store it in session state
                st.session_state.vectorstore = load_pdf(temp_file_path)
                os.remove(temp_file_path)  # Clean up the temp file
            except Exception as e:
                st.error(f"Error processing the file: {e}")

# Check if the vectorstore has been created
if st.session_state.vectorstore is not None:
    retriever = st.session_state.vectorstore.as_retriever()
    rag_chain = create_qa_pipeline(retriever)

    # Create chat input only if the vectorstore is loaded
    user_input = st.chat_input("Ask a question about your PDF file")
    # if st.button("Send"):
    if user_input:
        response = rag_chain.invoke({"input": user_input})
        st.write("**Question:**", user_input)
        st.write(response['answer'])  # Display the response


