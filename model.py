
from langchain_ollama import ChatOllama
from langchain_ollama import ChatOllama,OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma

model_name = 'qwen2.5:3b'
embedding_model_name = 'nomic-embed-text:latest'

def load_model():
    return ChatOllama(
        model=model_name,
        temperature=0.1,
        keep_alive="60m", # Keep in RAM for 1 hour so it's instant next time
        num_ctx=3072      # Slightly smaller window makes processing faster
    )
    


# ----------- INITILIZATION ---------- 
model = load_model()
parser = StrOutputParser()
embedding = OllamaEmbeddings(model=embedding_model_name)
