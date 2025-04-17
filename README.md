# Wealth Knowledge Bank

A document processing and question-answering system built with React, FastAPI, and LangChain.

## Features

- Upload and process PDF documents
- Automatic embedding generation using OpenAI's text-embedding-3-large model
- Question answering using GPT-4o
- Modern React frontend with Material-UI
- Incremental document processing
- Source document tracking

## Project Structure

```
wealth_knowledge_bank/
├── frontend/           # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.tsx
│   │   │   └── QuestionAnswer.tsx
│   │   └── App.tsx
│   └── package.json
├── backend/            # FastAPI backend
│   ├── main.py
│   └── requirements.txt
├── knowledge_assets/   # PDF documents
└── .env               # Environment variables
```

## Setup

### Backend

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:
   ```
   OPENAI_API_KEY=your_openai_api_key
   MODEL_NAME=gpt-4o
   EMBEDDING_MODEL=text-embedding-3-large
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   POSTGRES_HOST=your_postgres_host
   POSTGRES_PORT=your_postgres_port
   POSTGRES_DB=your_postgres_db
   POSTGRES_USER=your_postgres_user
   POSTGRES_PASSWORD=your_postgres_password
   ```

4. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Upload PDF documents using the drag-and-drop interface
3. Ask questions about the uploaded documents
4. View answers with source document references

## API Endpoints

### Backend

- `POST /upload`: Upload and process a PDF file
- `POST /ask`: Ask a question about the processed documents

## Technologies Used

- Frontend:
  - React
  - TypeScript
  - Material-UI
  - Axios
  - React Dropzone

- Backend:
  - FastAPI
  - LangChain
  - OpenAI
  - PostgreSQL with PGVector
  - Python

## License

MIT 