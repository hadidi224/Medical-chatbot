import os
import sys
import time
from langchain_community.llms import LlamaCpp

# Helper logging
def log(msg):
    print(f"\n[DEBUG] {msg}")
    sys.stdout.flush()

try:
    log("1. Testing LlamaCpp Initialization...")
    # Use absolute path for robustness
    model_path = r"c:\Users\USER\Desktop\Medical_chatbot\Medical_chatbot\Model\llama-2-7b-chat.Q4_K_M.gguf"
    
    if not os.path.exists(model_path):
        log(f"[FATAL] Model file not found at {model_path}")
        sys.exit(1)

    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.5,
        max_tokens=256,
        top_p=0.9,
        verbose=True,
        n_ctx=2048,
        n_gpu_layers=0,  # Force CPU
        n_batch=1,       # Process one token often
        n_threads=4      # Match app.py
    )
    log("   - Model loaded successfully.")

    log("2. Attempting generation...")
    start = time.time()
    res = llm.invoke("Hello, how are you?")
    log(f"   - Generation OK ({time.time() - start:.2f}s): {res}")

except Exception as e:
    log(f"   [FATAL] Error: {e}")
    sys.exit(1)
