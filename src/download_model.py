import os
from huggingface_hub import hf_hub_download

def download_model():
    model_name_or_path = "TheBloke/Llama-2-7B-Chat-GGUF"
    model_basename = "llama-2-7b-chat.Q4_K_M.gguf"
    
    print(f"Checking for model: {model_basename}")
    
    # Download the model to the local directory 'Model' if it doesn't exist
    model_path = hf_hub_download(
        repo_id=model_name_or_path,
        filename=model_basename,
        local_dir="Model",
        local_dir_use_symlinks=False
    )
    
    print(f"Model available at: {model_path}")
    return model_path

if __name__ == "__main__":
    download_model()
