import os
import sys

# Add project root to path if needed (though running from root is best)
sys.path.append(os.getcwd())

from langchain_community.llms import LlamaCpp

# Absolute path to model
model_path = r"c:\Users\USER\Desktop\Medical_chatbot\Medical_chatbot\Model\llama-2-7b-chat.Q4_K_M.gguf"

print(f"Checking model at: {model_path}")
if not os.path.exists(model_path):
    print("Model file not found!")
    sys.exit(1)

print("Loading LLM with LlamaCpp...")
try:
    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.5,
        max_tokens=256,
        top_p=0.9,
        verbose=True,
        n_ctx=2048,
        n_gpu_layers=0,
        n_batch=1,
        n_threads=4
    )
    print("LLM Loaded.")
except Exception as e:
    print(f"LLM Load Failed: {e}")
    sys.exit(1)

print("Generating...")
try:
    res = llm.invoke("Hello")
    print(f"Result: {res}")
except Exception as e:
    print(f"Generation Failed: {e}")

print("Done.")
