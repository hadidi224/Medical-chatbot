from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
import certifi
import threading
import time
import re
import string
from random import choice
from functools import lru_cache
# from langchain_community.llms import LlamaCpp

# --- LangChain Imports ---
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import pinecone
from src.prompt import prompt_template

import threading
import time

import re
import string
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
from random import choice


app = Flask(__name__)
load_dotenv()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
# Initialize Pinecone
#PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_KEY = 'pcsk_36Cf9k_6dB7RLsfjuJWGUJKkg6tJDLSCRSbqZc2AzukvvekD6E6jhxmPyGtdS8s556wafS'  # Set your actual key
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index_name = "medicaa"

embeddings = HuggingFaceEmbeddings(
   model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
   model_kwargs={'device': 'cpu'},
   encode_kwargs={
       'batch_size': 64,
       'normalize_embeddings': True,
    
    }
)

# Update your index configuration with these faster settings
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="dotproduct",  # Faster than cosine for some cases
        spec=pinecone.ServerlessSpec(
            cloud="aws",
            region="us-east-1",
            pod_type="s1.x1"  # Higher performance pod type
        )
    )
    # Wait for index to be ready
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
    #1
    # Only load and process documents if creating new index
    def load_pdf(data):
        loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
        return loader.load()
    #2
    def text_split(documents):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=20)
        return text_splitter.split_documents(documents)

    documents = load_pdf("data/")
    text_chunks = text_split(documents)
   #4 
    # Create vector store (one-time operation)
    PineconeVectorStore.from_documents(
        documents=text_chunks,
        embedding=embeddings,
        index_name=index_name
    )
    print("Vector store created and persisted in Pinecone")

# Now always connect to existing index
# Now always connect to existing index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
print("Connected to existing Pinecone index")


print("Pinecone index stats:", docsearch._index.describe_index_stats())

# Rest of your QA chain setup
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}


 

#6
from langchain_groq import ChatGroq

# llm = CTransformers(
#     model="Model/llama-2-7b-chat.Q4_K_M.gguf",
#     model_type="llama",
#     ...
# )

print("Loading LLM with ChatGroq (Ultra-Fast Mode)...")
GROQ_API_KEY = os.getenv('GROQ_API_KEY') or "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"

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant", # Or "llama3-70b-8192" for higher quality
    temperature=0.2,
    max_tokens=512,
)

# Replace your pre-warm code with this safer version:
print("Pre-warming components...")
try:
    # Simple query that should work with any index
    warmup_query = "health"
    docs = docsearch.similarity_search(warmup_query, k=1)
    print(f"Pre-warm retrieved {len(docs)} documents")
    
    # Test LLM with short prompt
    test_output = llm.invoke("Hello")
    print("LLM test output:", test_output[:50] + "...")
    
    print("System ready")
except Exception as e:
    print(f"Pre-warm warning: {str(e)}")
    print("System starting with partial warm-up")

@app.route("/")
def index():
    return render_template('chat.html')

# Update your imports (keep existing ones and add these)
from typing import Dict, Any
import time
#5
# Update your retriever configuration
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(
        search_kwargs={
            'k': 4,  # Groq can handle more context effortlessly
        }
    ),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)


def prioritize_response(query: str) -> str:
    """Faster response for common queries"""
    common_responses = {
        "hello": "Hello! How can I assist you with medical questions today?",
        "hi": "Hi there! What medical information are you looking for?",
        "thanks": "You're welcome! Let me know if you have other questions.",
        "thank you": "You're welcome! Let me know if you have other questions.",
        "bye": "Goodbye! Take care and stay healthy!",
        "goodbye": "Goodbye! Take care and stay healthy!",
        "hey": "Hello! How can I help you today?",
        "morning": "Good morning! What medical questions can I answer for you?",
        "evening": "Good evening! How can I assist you with health information?"
    }
    return common_responses.get(query, None)

def clean_input(text: str) -> str:
    """Normalize user input for matching"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text

@lru_cache(maxsize=128)
def get_cached_answer(query: str) -> str:
    result = qa.invoke({"query": query})
    return result["result"]


@app.route("/get", methods=["POST"])
def chat():
    try:
        msg = request.form.get("msg", "").strip()
        if not msg:
            return "Please enter a valid question"
        
        cleaned_msg = clean_input(msg)
        print(f"\n[USER]: {msg} (cleaned: {cleaned_msg})")

        # 1. Quick response for greetings/common phrases
        quick_response = prioritize_response(cleaned_msg)
        if quick_response:
            print(f"[BOT]: {quick_response} (Quick Response)")
            return quick_response
        
        # 2. Process with RAG chain
        print("Searching knowledge base...")
        result = qa.invoke({"query": msg})
        
        answer = result["result"]
        source_docs = result.get("source_documents", [])
        
        print(f"Retrieved {len(source_docs)} documents.")
        print(f"[BOT]: {answer}")
        return answer
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return "Sorry, I encountered an error. Please try again in a moment."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)