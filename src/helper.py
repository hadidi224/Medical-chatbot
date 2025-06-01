from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import os
import certifi
import sentence_transformers

import ssl
from langchain_community.embeddings import HuggingFaceEmbeddings

#Extract data from the PDF
def load_pdf(data):
    loader = DirectoryLoader(data,
                    glob="*.pdf",
                    loader_cls=PyPDFLoader)
    
    documents = loader.load()

    return documents


#Create text chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks


#download embedding model
from langchain.embeddings import HuggingFaceEmbeddings

def download_hugging_face_embeddings(use_local=False, local_path=None):
    # Disable SSL verification (temporary solution)
    
    """
    Download or load Hugging Face embeddings with SSL fixes
    
    Args:
        use_local (bool): If True, loads from local path
        local_path (str): Absolute path to local model (required if use_local=True)
    """
    # ===== SSL FIX (Choose one method) =====
    # Method 1: Use certifi's CA bundle (recommended)
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    # Method 2: Temporary SSL bypass (uncomment if needed)
    os.environ['CURL_CA_BUNDLE'] = ''
    
    try:
        if use_local:
            # ===== LOCAL MODEL LOADING =====
            if not local_path or not os.path.exists(local_path):
                raise ValueError(f"Model not found at: {local_path}")
                
            print(f"Loading local model from: {local_path}")
            embeddings = HuggingFaceEmbeddings(
                model_name=local_path,
                model_kwargs={'device': 'cpu'},  # or 'cuda' for GPU
                encode_kwargs={'normalize_embeddings': False}
            )
        else:
            # ===== DOWNLOAD FROM HUGGING FACE =====
            print("Downloading model from Hugging Face Hub...")
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': False}
            )
            
        # Test the embeddings
        test_text = "This is a test sentence."
        embedding = embeddings.embed_query(test_text)
        print(f"Embedding test successful! Vector length: {len(embedding)}")
        
        return embeddings
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

