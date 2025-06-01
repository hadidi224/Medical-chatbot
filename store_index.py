# from src.helper import load_pdf, text_split, download_hugging_face_embeddings
# from langchain.vectorstores import Pinecone
# import pinecone
# from dotenv import load_dotenv
# import os
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain import PromptTemplate
# from langchain.chains import RetrievalQA
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import Pinecone
# import pinecone
# from langchain.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate
# from langchain.llms import CTransformers

# load_dotenv()

# import os
# from pinecone import Pinecone, ServerlessSpec
# from langchain_pinecone import PineconeVectorStore 

# # 1. Set your API key (best practice is environment variables)
# os.environ['PINECONE_API_KEY'] = 'pcsk_36Cf9k_6dB7RLsfjuJWGUJKkg6tJDLSCRSbqZc2AzukvvekD6E6jhxmPyGtdS8s556wafS'  # Set your actual key
# PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

# # 2. Initialize Pinecone client
# pc = Pinecone(api_key=PINECONE_API_KEY)

# #Extract data from the PDF
# def load_pdf(data):
#     loader = DirectoryLoader(data,
#                     glob="*.pdf",
#                     loader_cls=PyPDFLoader)
    
#     documents = loader.load()

#     return documents

# # 3. Create index configuration
# index_name = "medica"

# #Create text chunks
# def text_split(extracted_data):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
#     text_chunks = text_splitter.split_documents(extracted_data)

#     return text_chunks


# if index_name not in pc.list_indexes().names():
#     pc.create_index(
#         name=index_name,
#         dimension=384,  # Must match your embedding model's output dim
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud="aws",
#             region="us-east-1"  # Free tier compatible region
#         )
#     )

# # 4. Wait for index to be ready
# import time
# while not pc.describe_index(index_name).status['ready']:
#     print("Waiting for index initialization...")
#     time.sleep(5)

# # 5. Create vector store with explicit API key
# docsearch = PineconeVectorStore.from_texts(
#     texts=[t.page_content for t in text_chunks],
#     embedding=embeddings,
#     index_name=index_name,
#     pinecone_api_key=PINECONE_API_KEY  # Critical addition
# )

# print("Successfully created vector store!") 