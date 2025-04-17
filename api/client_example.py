import requests
import json

# API configuration
API_BASE_URL = "http://localhost:8000"

def upload_document(file_path):
    """Upload a PDF document to the API"""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{API_BASE_URL}/upload", files=files)
        return response.json()

def ask_question(question):
    """Ask a question about the processed documents"""
    response = requests.post(
        f"{API_BASE_URL}/ask",
        json={"question": question}
    )
    return response.json()

def get_status():
    """Get the current processing status"""
    response = requests.get(f"{API_BASE_URL}/status")
    return response.json()

# Example usage
if __name__ == "__main__":
    # Upload a document
    print("Uploading document...")
    upload_result = upload_document("knowledge_assets/example.pdf")
    print("Upload result:", json.dumps(upload_result, indent=2))
    
    # Ask a question
    print("\nAsking question...")
    question = "What is the main topic of the document?"
    answer = ask_question(question)
    print(f"Question: {question}")
    print("Answer:", json.dumps(answer, indent=2))
    
    # Check status
    print("\nChecking status...")
    status = get_status()
    print("Status:", json.dumps(status, indent=2)) 