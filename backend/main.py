from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores.pgvector import PGVector
import urllib.parse
import json
import hashlib
from datetime import datetime
from typing import List, Optional

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    text: str

class Answer(BaseModel):
    answer: str
    sources: List[dict]

def get_file_hash(file_path: str) -> str:
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def load_processing_state() -> dict:
    """Load the processing state from JSON file"""
    try:
        with open('processing_state.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"processed_files": {}}

def save_processing_state(state: dict) -> None:
    """Save the processing state to JSON file"""
    with open('processing_state.json', 'w') as f:
        json.dump(state, f, indent=4)

def get_connection_string() -> str:
    """Get PostgreSQL connection string"""
    password = urllib.parse.quote(os.getenv('POSTGRES_PASSWORD'))
    return f"postgresql://postgres:{password}@db.klmchbozebcmpgytlqhf.supabase.co:6543/postgres"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    try:
        # Save the uploaded file
        file_path = f"knowledge_assets/{file.filename}"
        os.makedirs("knowledge_assets", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process the file
        state = load_processing_state()
        file_hash = get_file_hash(file_path)
        
        # Check if file needs processing
        if file_path in state["processed_files"] and state["processed_files"][file_path]["hash"] == file_hash:
            return {"message": "File already processed", "file": file.filename}
        
        # Process the file
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=int(os.getenv('CHUNK_SIZE', 1000)),
            chunk_overlap=int(os.getenv('CHUNK_OVERLAP', 200))
        )
        chunks = text_splitter.split_documents(documents)
        
        # Create embeddings and store in PostgreSQL
        connection_string = get_connection_string()
        embeddings = OpenAIEmbeddings(
            model=os.getenv('EMBEDDING_MODEL', 'text-embedding-3-large')
        )
        
        vector_store = PGVector.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name="document_embeddings",
            connection_string=connection_string,
            pre_delete_collection=False
        )
        
        # Update processing state
        state["processed_files"][file_path] = {
            "hash": file_hash,
            "last_processed": datetime.now().isoformat()
        }
        save_processing_state(state)
        
        return {"message": "File processed successfully", "file": file.filename, "chunks": len(chunks)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    """Answer a question using the processed documents"""
    try:
        connection_string = get_connection_string()
        embeddings = OpenAIEmbeddings(
            model=os.getenv('EMBEDDING_MODEL', 'text-embedding-3-large')
        )
        
        vector_store = PGVector(
            collection_name="document_embeddings",
            connection_string=connection_string,
            embedding_function=embeddings
        )
        
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        llm = ChatOpenAI(
            model_name=os.getenv('MODEL_NAME', 'gpt-4o'),
            temperature=0
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        
        response = qa_chain.invoke({"query": question.text})
        
        sources = []
        for doc in response.get('source_documents', []):
            sources.append({
                "page": doc.metadata.get('page', 'N/A'),
                "file": doc.metadata.get('source', 'N/A'),
                "content": doc.page_content
            })
        
        return Answer(
            answer=response['result'],
            sources=sources
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 