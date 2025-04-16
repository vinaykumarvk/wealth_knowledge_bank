# Document Question Answering System

This application allows you to ask questions about your PDF documents and get accurate answers using AI.

## Features

- Process multiple PDF documents
- Create a searchable knowledge base using PostgreSQL
- Ask questions in natural language
- Get accurate answers based on document content

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up PostgreSQL:
   ```bash
   # Install PostgreSQL if not already installed
   # For macOS:
   brew install postgresql
   # For Ubuntu:
   sudo apt-get install postgresql postgresql-contrib

   # Start PostgreSQL service
   # For macOS:
   brew services start postgresql
   # For Ubuntu:
   sudo service postgresql start

   # Create database and user
   psql -U postgres
   CREATE DATABASE vector_db;
   CREATE USER your_username WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE vector_db TO your_username;
   \q

   # Install pgvector extension
   psql -U your_username -d vector_db
   CREATE EXTENSION vector;
   \q
   ```

4. Create a `.env` file based on `.env.example` and add your OpenAI API key and PostgreSQL credentials
5. Place your PDF documents in the `knowledge_assets` directory

## Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```
2. Click the "Process Documents" button in the sidebar to create the knowledge base
3. Enter your question in the main interface
4. Get your answer!

## Requirements

- Python 3.8+
- OpenAI API key
- PostgreSQL with pgvector extension
- PDF documents to process (placed in the `knowledge_assets` directory)

## Note

The first time you process documents, it may take a few minutes depending on the size of your PDF files. This is because the system needs to:
1. Extract text from PDFs
2. Split the text into manageable chunks
3. Create vector embeddings
4. Store them in PostgreSQL with pgvector

Subsequent questions will be answered much faster as the knowledge base is already created in the database. 