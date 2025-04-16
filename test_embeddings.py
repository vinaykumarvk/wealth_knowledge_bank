import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
import urllib.parse

# Load environment variables
load_dotenv()

def get_connection_string():
    """Get PostgreSQL connection string"""
    password = urllib.parse.quote(os.getenv('POSTGRES_PASSWORD'))
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    db = os.getenv('POSTGRES_DB')
    user = os.getenv('POSTGRES_USER')
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"

def test_embeddings():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(get_connection_string())
        cur = conn.cursor()
        
        # Check if the collection exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'document_embeddings'
            );
        """)
        collection_exists = cur.fetchone()[0]
        
        if not collection_exists:
            print("Error: Document embeddings collection does not exist!")
            return
        
        # Count the number of embeddings
        cur.execute("SELECT COUNT(*) FROM document_embeddings;")
        count = cur.fetchone()[0]
        print(f"Number of document embeddings in database: {count}")
        
        # Get sample embeddings
        cur.execute("""
            SELECT metadata, embedding 
            FROM document_embeddings 
            LIMIT 1;
        """)
        sample = cur.fetchone()
        
        if sample:
            print("\nSample document metadata:")
            print(sample[0])  # metadata
            print(f"\nEmbedding vector length: {len(sample[1])}")  # embedding vector length
        
        # Close connections
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error testing embeddings: {str(e)}")

if __name__ == "__main__":
    test_embeddings() 