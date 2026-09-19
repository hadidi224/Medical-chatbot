import os
import sys
import time

# Helper logging
def log(msg):
    print(f"\n[DEBUG] {msg}")
    sys.stdout.flush()

try:
    log("1. Importing libraries...")
    from langchain_community.llms import CTransformers
    from langchain_huggingface import HuggingFaceEmbeddings
    # from langchain_pinecone import PineconeVectorStore # Defer import
    import certifi
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    log("   - Libraries imported successfully.")
except Exception as e:
    log(f"   [FATAL] Import failed: {e}")
    sys.exit(1)

# --- Test 1: Embeddings ---
log("2. Testing Embeddings (HuggingFace)...")
try:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    res = embeddings.embed_query("This is a test sentence for embeddings.")
    log(f"   - Embeddings OK. Vector dimension: {len(res)}")
except Exception as e:
    log(f"   [FATAL] Embeddings failed: {e}")
    sys.exit(1)

# --- Test 2: LLM (The likely suspect) ---
log("3. Testing LLM (CTransformers)...")
try:
    llm = CTransformers(
        model="TheBloke/Llama-2-7B-Chat-GGUF",
        model_file="llama-2-7b-chat.Q4_K_M.gguf",
        model_type="llama",
        config={
            'max_new_tokens': 64,
            'temperature': 0.5,
            'gpu_layers': 0,
            'threads': 1,      # REDUCED TO 1 FOR STABILITY
            'batch_size': 1,
            'context_length': 512
        }
    )
    log("   - Model loaded into memory.")
    
    log("   - Attempting generation...")
    start = time.time()
    res = llm.invoke("Explain fever in one sentence.")
    log(f"   - Generation OK ({time.time() - start:.2f}s): {res.strip()}")
except Exception as e:
    log(f"   [FATAL] LLM Generation failed: {e}")
    sys.exit(1)

log("--------------------------------------------------")
log("ALL INDIVIDUAL COMPONENTS PASSED.")
log("If it crashes in the app but not here, it is likely the Pinecone/Chain interaction.")
log("--------------------------------------------------")
