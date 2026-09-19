import os
import sys

# Set environment variables that might help debug
os.environ['Llama_CPP_VERBOSE'] = '1'

def log(msg):
    print(f"[REPRO] {msg}")
    sys.stdout.flush()

log("1. Importing modules...")
try:
    # 1. Import Torch-heavy things first (like app.py)
    from langchain_huggingface import HuggingFaceEmbeddings
    log("   - HuggingFaceEmbeddings imported.")
    
    # 2. Initialize Embeddings (loads Torch/MKL)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
        model_kwargs={'device': 'cpu'}
    )
    # Run a quick embed to force library load
    _ = embeddings.embed_query("warmup")
    log("   - HuggingFaceEmbeddings initialized and warmed up.")
except Exception as e:
    log(f"   [ERROR] Embeddings failed: {e}")

try:
    # 3. Import LlamaCpp
    from langchain_community.llms import LlamaCpp
    log("   - LlamaCpp imported.")

    model_path = r"c:\Users\USER\Desktop\Medical_chatbot\Medical_chatbot\Model\llama-2-7b-chat.Q4_K_M.gguf"
    if not os.path.exists(model_path):
        log("   [ERROR] Model file not found!")
        sys.exit(1)

    # 4. Initialize LlamaCpp
    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.5,
        max_tokens=50,
        n_ctx=512,
        n_gpu_layers=0,
        n_batch=1,
        n_threads=4,
        verbose=True
    )
    log("   - LlamaCpp initialized.")

    # 5. Generate
    log("2. Attempting generation (CROSS-FINGERS)...")
    res = llm.invoke("Hello, medical bot.")
    log(f"   - Generation Result: {res}")

except Exception as e:
    log(f"   [CRASH/ERROR] {e}")

log("Done.")
