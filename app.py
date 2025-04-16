import os
import streamlit as st
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores.pgvector import PGVector
import urllib.parse

# Load environment variables
load_dotenv()

# Initialize session state
if 'retriever' not in st.session_state:
    st.session_state.retriever = None

def get_connection_string():
    """Get PostgreSQL connection string"""
    password = urllib.parse.quote(os.getenv('POSTGRES_PASSWORD'))
    return f"postgresql://postgres:{password}@db.klmchbozebcmpgytlqhf.supabase.co:6543/postgres"

def process_documents():
    """Process PDF documents and store in PostgreSQL"""
    st.info("Processing documents...")
    
    # Get all PDF files from the knowledge_assets directory
    knowledge_dir = 'knowledge_assets'
    pdf_files = [os.path.join(knowledge_dir, f) for f in os.listdir(knowledge_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        st.error("No PDF files found in the knowledge_assets directory!")
        return
    
    try:
        # Load and process documents
        documents = []
        for pdf_file in pdf_files:
            with st.status(f"Processing {os.path.basename(pdf_file)}..."):
                loader = PyPDFLoader(pdf_file)
                documents.extend(loader.load())
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=int(os.getenv('CHUNK_SIZE', 1000)),
            chunk_overlap=int(os.getenv('CHUNK_OVERLAP', 200))
        )
        chunks = text_splitter.split_documents(documents)
        
        # Create vector store in PostgreSQL
        connection_string = get_connection_string()
        embeddings = OpenAIEmbeddings(
            model=os.getenv('EMBEDDING_MODEL', 'text-embedding-3-large')
        )
        
        # Store document chunks in PostgreSQL
        with st.status("Creating vector embeddings and storing in database..."):
            vector_store = PGVector.from_documents(
                documents=chunks,
                embedding=embeddings,
                collection_name="document_embeddings",
                connection_string=connection_string,
                pre_delete_collection=True  # Clear existing collection
            )
            
            # Save retriever in session state
            st.session_state.retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}  # Return top 3 most relevant chunks
            )
        
        st.success(f"Successfully processed {len(chunks)} document chunks!")
        
    except Exception as e:
        st.error(f"Error processing documents: {str(e)}")

def get_answer(question):
    """Get answer for the given question"""
    if st.session_state.retriever is None:
        st.error("Please process documents first!")
        return
    
    try:
        # Create QA chain
        llm = ChatOpenAI(
            model_name=os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
            temperature=0
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=st.session_state.retriever,
            return_source_documents=True  # Include source documents in response
        )
        
        # Get answer
        response = qa_chain.invoke({"query": question})
        
        # Display answer and sources
        st.write("### Answer:")
        st.write(response['result'])
        
        # Display source documents
        st.write("### Sources:")
        sources = response.get('source_documents', [])
        for i, doc in enumerate(sources, 1):
            st.write(f"**Source {i}:**")
            st.write(f"- Page: {doc.metadata.get('page', 'N/A')}")
            st.write(f"- File: {doc.metadata.get('source', 'N/A')}")
            with st.expander("Show source text"):
                st.write(doc.page_content)
        
    except Exception as e:
        st.error(f"Error getting answer: {str(e)}")

def main():
    st.title("Document Question Answering System")
    
    # Sidebar for document processing
    with st.sidebar:
        st.header("Document Processing")
        if st.button("Process Documents"):
            process_documents()
    
    # Main content area
    st.header("Ask Questions")
    question = st.text_input("Enter your question:")
    
    if question:
        with st.spinner("Searching for answers..."):
            get_answer(question)

if __name__ == "__main__":
    main() 