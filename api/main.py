from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
from datetime import datetime
from pathlib import Path
import shutil
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import PyPDF2
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Wealth Nowledge Bank API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Configuration
CONNECTION_STRING = f"postgresql+psycopg2://postgres:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/postgres"
COLLECTION_NAME = "document_embeddings"
KNOWLEDGE_ASSETS_DIR = "knowledge_assets"
PROCESSING_STATE_FILE = "processing_state.json"

# Initialize models
llm = ChatOpenAI(
    model_name=os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
    temperature=0
)
embeddings = OpenAIEmbeddings(model=os.getenv('EMBEDDING_MODEL', 'text-embedding-3-large'))

# Pydantic models for request/response
class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str
    sources: List[str]

class ProcessingStatus(BaseModel):
    status: str
    processed_files: List[str]
    last_processed: Optional[str]

# Helper functions
def get_processing_state():
    if os.path.exists(PROCESSING_STATE_FILE):
        with open(PROCESSING_STATE_FILE, 'r') as f:
            return json.load(f)
    return {"processed_files": [], "last_processed": None}

def save_processing_state(state):
    with open(PROCESSING_STATE_FILE, 'w') as f:
        json.dump(state, f)

def process_document(file_path: str):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=int(os.getenv('CHUNK_SIZE', 1000)),
                chunk_overlap=int(os.getenv('CHUNK_OVERLAP', 200))
            )
            chunks = text_splitter.split_text(text)
            
            # Store embeddings in PostgreSQL
            PGVector.from_texts(
                texts=chunks,
                embedding=embeddings,
                collection_name=COLLECTION_NAME,
                connection_string=CONNECTION_STRING,
                pre_delete_collection=False
            )
            
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

# API Endpoints
@app.post("/upload", response_model=ProcessingStatus)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Save uploaded file
    file_path = os.path.join(KNOWLEDGE_ASSETS_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process document
    success = process_document(file_path)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to process document")
    
    # Update processing state
    state = get_processing_state()
    state["processed_files"].append(file.filename)
    state["last_processed"] = datetime.now().isoformat()
    save_processing_state(state)
    
    return ProcessingStatus(
        status="success",
        processed_files=state["processed_files"],
        last_processed=state["last_processed"]
    )

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    try:
        # Create vector store
        vectorstore = PGVector(
            collection_name=COLLECTION_NAME,
            connection_string=CONNECTION_STRING,
            embedding_function=embeddings
        )
        
        # Create retriever
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        # Create prompt template
        template = """Answer the question based on the following context:
        {context}
        
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        # Create chain
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        # Get answer
        answer = chain.invoke(question.question)
        
        # Get source documents
        docs = retriever.get_relevant_documents(question.question)
        sources = [doc.metadata.get('source', 'Unknown') for doc in docs]
        
        return Answer(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status", response_model=ProcessingStatus)
async def get_status():
    state = get_processing_state()
    return ProcessingStatus(
        status="success",
        processed_files=state["processed_files"],
        last_processed=state["last_processed"]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 