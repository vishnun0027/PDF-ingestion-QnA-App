from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from llm import llm, hf_embeddings

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llm import hf_embeddings

# Load the PDF document
def load_pdf(file_path):
    """
    Function to load a PDF document and return a list of Document objects.

    Args:
    file_path (str): The path to the PDF file.

    Returns:
    list: A list of Document objects representing the loaded PDF.
    """
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Create an in-memory vector store with embeddings
    vectorstore = InMemoryVectorStore.from_documents(
        documents=splits, embedding=hf_embeddings
    )
    return vectorstore

# retriever = vectorstore.as_retriever()

def create_qa_pipeline(retriever):
    """
    Function to create a question-answering pipeline using a language model
    and a retriever for document context.
    
    Args:
    llm: The language model to use for generating answers.
    retriever: A retriever object that fetches relevant document chunks.
    
    Returns:
    rag_chain: The complete retrieval-augmented generation (RAG) chain.
    """
    # Define the system prompt for the assistant
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    # Create a chat prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # Create a question-answering chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    # Create the retrieval chain
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain

