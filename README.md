# Wealth Nowledge Bank

A document question answering system that processes PDF documents and answers questions based on their content.

## Features

- Process PDF documents from the `knowledge_assets` directory
- Incremental processing of new or modified documents
- Question answering using OpenAI's GPT models
- Source document references for answers
- Persistent storage using PostgreSQL with pgvector

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

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Click "Process Documents" in the sidebar to process your PDF files

4. Enter your question in the text input field and press Enter

## Project Structure

- `app.py`: Main Streamlit application
- `requirements.txt`: Python dependencies
- `knowledge_assets/`: Directory for PDF documents
- `.env`: Environment variables
- `processing_state.json`: Tracks processed documents
- `test_db.py`: Database connection test script
- `test_embeddings.py`: Embeddings test script

## Dependencies

- streamlit
- langchain
- openai
- python-dotenv
- pgvector
- python-multipart
- PyPDF2

## License

MIT 