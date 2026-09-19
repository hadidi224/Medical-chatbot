import os
import sys

print("1. Testing Imports...")
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    print("   - HuggingFaceEmbeddings imported.")
except ImportError as e:
    print(f"   - Failed to import HuggingFaceEmbeddings: {e}")

try:
    from langchain_community.llms import CTransformers
    print("   - CTransformers imported.")
except ImportError as e:
    print(f"   - Failed to import CTransformers: {e}")

print("\n2. Testing Embeddings (Torch)...")
try:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
        model_kwargs={'device': 'cpu'}
    )
    res = embeddings.embed_query("test")
    print(f"   - Embedding success. Vector length: {len(res)}")
except Exception as e:
    print(f"   - Embedding FAILED: {e}")

print("\n3. Testing LLM (CTransformers/Llama.cpp)...")
try:
    llm = CTransformers(
        model="TheBloke/Llama-2-7B-Chat-GGUF",
        model_file="llama-2-7b-chat.Q4_K_M.gguf",
        model_type="llama",
        config={'gpu_layers': 0, 'threads': 2}
    )
    print("   - Model loaded.")
    res = llm.invoke("Hello")
    print(f"   - Generation success: {res}")
except Exception as e:
    print(f"   - LLM FAILED: {e}")

print("\nDone.")
