# Wealth Nowledge Bank

A document question answering system that processes PDF documents and answers questions based on their content.

## Features

- Process PDF documents from the `knowledge_assets` directory
- Incremental processing of new or modified documents
- Question answering using OpenAI's GPT models
- Source document references for answers
- Persistent storage using PostgreSQL with pgvector
- REST API for integration with other applications

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wealth_nowledge_bank.git
cd wealth_nowledge_bank
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with your environment variables:
```bash
cp .env.example .env
```
Then edit `.env` with your actual values:
```
OPENAI_API_KEY=your_openai_api_key
POSTGRES_PASSWORD=your_postgres_password
MODEL_NAME=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-3-large
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

4. Place your PDF documents in the `knowledge_assets` directory.

## Usage

### Streamlit Interface

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Click "Process Documents" in the sidebar to process your PDF files

4. Enter your question in the text input field and press Enter

### API Usage

1. Start the API server:
```bash
cd api
pip install -r requirements.txt
python main.py
```

2. The API will be available at `http://localhost:8000`

3. API Endpoints:

   - `POST /upload`: Upload and process a PDF file
     ```bash
     curl -X POST -F "file=@path/to/document.pdf" http://localhost:8000/upload
     ```

   - `POST /ask`: Ask a question about the processed documents
     ```bash
     curl -X POST -H "Content-Type: application/json" \
          -d '{"question": "What is the main topic?"}' \
          http://localhost:8000/ask
     ```

   - `GET /status`: Get the current processing status
     ```bash
     curl http://localhost:8000/status
     ```

4. Example Python client usage:
```python
from api.client_example import upload_document, ask_question, get_status

# Upload a document
upload_result = upload_document("knowledge_assets/example.pdf")

# Ask a question
answer = ask_question("What is the main topic?")

# Check status
status = get_status()
```

## Project Structure

- `app.py`: Main Streamlit application
- `api/`: API implementation
  - `main.py`: FastAPI application
  - `requirements.txt`: API dependencies
  - `client_example.py`: Example API client
- `requirements.txt`: Python dependencies
- `knowledge_assets/`: Directory for PDF documents
- `.env`: Environment variables
- `processing_state.json`: Tracks processed documents
- `test_db.py`: Database connection test script
- `test_embeddings.py`: Embeddings test script

## Dependencies

- streamlit
- fastapi
- langchain
- openai
- python-dotenv
- pgvector
- python-multipart
- PyPDF2

## License

MIT 