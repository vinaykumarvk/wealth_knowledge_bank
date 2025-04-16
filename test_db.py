import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import urllib.parse

# Load environment variables
load_dotenv()

def get_connection():
    """Get PostgreSQL connection"""
    # URL encode the password to handle special characters
    password = urllib.parse.quote(os.getenv('POSTGRES_PASSWORD'))
    connection_string = f"postgresql://postgres:{password}@db.klmchbozebcmpgytlqhf.supabase.co:6543/postgres"
    
    return psycopg2.connect(
        connection_string,
        sslmode='require'  # Required for Supabase
    )

def setup_pgvector():
    """Set up pgvector extension in the database"""
    try:
        # Connect to the database
        conn = get_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Test connection
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✅ Connected to PostgreSQL. Version: {version[0]}")
        
        # Enable pgvector extension
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        print("✅ pgvector extension enabled")
        
        # Create a test table with vector column
        cur.execute("""
            CREATE TABLE IF NOT EXISTS test_vectors (
                id SERIAL PRIMARY KEY,
                embedding vector(1536)
            );
        """)
        print("✅ Test table created successfully!")
        
        # Clean up
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("Testing PostgreSQL connection and setting up pgvector...")
    setup_pgvector() 