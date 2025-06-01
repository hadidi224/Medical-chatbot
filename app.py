from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore


import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter

# With these updated imports:
from langchain_community.vectorstores import Pinecone
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.llms import CTransformers
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
import torch

import certifi


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
embeddings = download_hugging_face_embeddings()
#sentence-transformers/paraphrase-MiniLM-L3-v2
#sentence-transformers/all-MiniLM-L6-v2
#embeddings = HuggingFaceEmbeddings(
 #   model_name="sentence-transformers/all-MiniLM-L6-v2",
  #  model_kwargs={'device': 'cpu'},
   # encode_kwargs={
    #    'batch_size': 64,
     #   'normalize_embeddings': True,
    
    #}
#)

# Expand with basic synonyms
def expand_query(query):
    words = query.split()
    expanded = []
    for word in words:
        syns = wordnet.synsets(word)
        if syns:
            expanded.append(syns[0].lemmas()[0].name())
        else:
            expanded.append(word)
    return " ".join(expanded)



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
    
    # Only load and process documents if creating new index
    def load_pdf(data):
        loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
        return loader.load()

    def text_split(documents):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=20)
        return text_splitter.split_documents(documents)

    documents = load_pdf("data/")
    text_chunks = text_split(documents)
    
    # Create vector store (one-time operation)
    PineconeVectorStore.from_documents(
        documents=text_chunks,
        embedding=embeddings,
        index_name=index_name
    )
    print("Vector store created and persisted in Pinecone")

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


from ctransformers import AutoModelForCausalLM 


llm = CTransformers(
    model="TheBloke/Llama-2-7B-Chat-GGML",
    model_file="llama-2-7b-chat.ggmlv3.q4_0.bin",
    model_type="llama",
    config={
        'max_new_tokens': 128,  # Reduced from 256
        'temperature': 0.5,     # Reduced from 0.7 for more deterministic answers
        'top_p': 0.9,          # Add top-p sampling
        'gpu_layers': 40 if torch.cuda.is_available() else 0,
        'threads': min(4, os.cpu_count()),  # Limit CPU threads
        'batch_size': 1,        # Process one at a time
        'stream': False        # Disable streaming for faster completion
    }
)


#test_result = qa.invoke({"query": "What is acne?"})
#print(test_result)

#rint(llm("Hello"))  # Should return a response

#docs = docsearch.similarity_search("What is acne?", k=2)
#print(docs)

# Replace your pre-warm code with this safer version:
print("Pre-warming components...")
try:
    # Simple query that should work with any index
    warmup_query = "health"
    docs = docsearch.similarity_search(warmup_query, k=1)
    print(f"Pre-warm retrieved {len(docs)} documents")
    
    # Test LLM with short prompt
    test_output = llm("Hello")
    print("LLM test output:", test_output[:50] + "...")
    
    print("System ready")
except Exception as e:
    print(f"Pre-warm warning: {str(e)}")
    print("System starting with partial warm-up")

@app.route("/")
def index():
    return render_template('chat.html')

#@app.route("/get", methods=["GET", "POST"])
#def chat():
#    msg = request.form["msg"]
#    input = msg
#    print(input)
#    result = qa.invoke({"query": input})
#    print("Response : ", result["result"])
#    return str(result["result"])


#@app.route("/get", methods=["GET", "POST"])
#def chat():
#    msg = request.form["msg"]
#    print("Received input:", msg)

    # Check for quick responses first
 #   quick_response = prioritize_response(msg)
  #  if quick_response:
   #     return quick_response


    # Step 1: Clean input
    #cleaned_msg = clean_input(msg)
    #p#rint("Cleaned input:", cleaned_msg)

    # Step 2: (Optional) Expand query semantically
   # expanded_msg = expand_query(cleaned_msg)
   # print("Expanded input:", expanded_msg)
    

   # try:
        # Step 3: Query LLM through RetrievalQA chain
   #     result = qa.invoke({"query": expanded_msg})

        # Step 4: Post-process response
    #    final_response = polish_response(result["result"])
 #       print("Response:", final_response)
#
  #      return str(final_response)
   # except Exception as e:
    #    print("Error:", str(e))
     #   return "Sorry, I encountered an error processing your request."
# Update your imports (keep existing ones and add these)
from typing import Dict, Any
import time

# Update your retriever configuration
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(
        search_kwargs={
            'k': 2,  # Number of documents to retrieve
            # Pinecone-specific optimized parameters
            'filter': {'doc_length': {'$lt': 500}},
            # Remove unsupported parameters
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

@app.route("/get", methods=["POST"])
def chat():
    try:
        msg = request.form.get("msg", "").strip()
        if not msg:
            return "Please enter a valid question"
        
        cleaned_msg = clean_input(msg)
        
        # Check for quick responses first
        quick_response = prioritize_response(cleaned_msg)
        if quick_response:
            return quick_response
        
        # Process full query if no quick response
        result = qa.invoke({"query": msg})
        return result["result"]  # Return just the text response
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Sorry, I encountered an error processing your request"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)