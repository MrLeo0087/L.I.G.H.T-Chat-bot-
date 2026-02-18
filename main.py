# ------------- LIBRARY ------------------
print("Import File ....")
from langchain_ollama import ChatOllama
from langchain_ollama import ChatOllama,OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
import os
import sys

# --- LOCAL IMPORT ---
from promt import promt_general,promt_decide,prompt
from RAG_PDF.parent_child import database_action, DB_PATH
from key_word import RAG_KEYWORDS,NOT_RAG_KEYWORDS
from supportive_function import multi_query_generator

# --------- BASE ---------
print("Model Loading ..... ")
model_name = 'qwen2.5:3b'
embedding_model_name = 'nomic-embed-text:latest'

# DATA_BASE_PDF = ("./pdf_vector_store")
# os.makedirs(DATA_BASE_PDF,exist_ok=True)

def load_model():
    return ChatOllama(
        model=model_name,
        temperature=0.1,
        # keep_alive="60m", # Keep in RAM for 1 hour so it's instant next time
        num_ctx=3072      
    )

# ----------- INITILIZATION ---------- 
model = load_model()
parser = StrOutputParser()
embedding = OllamaEmbeddings(model=embedding_model_name)

# -- USE LOCAL FUNCTION -- 
PDF_PATH = r"D:\Learning\GenAI\LangChain\Practice\RAG\ATAYN.pdf"
if os.path.exists(PDF_PATH):
    vector_database = database_action(PDF_PATH,embedding)

else:
    print("ERROR: PDF PATH NOT FOUND! ")



# Change search_type to "mmr"
# base_retriever = vector_database.as_retriever(
#     search_type="mmr", 
#     search_kwargs={'k': 3, 'fetch_k': 7}
# )

base_retriever = vector_database.as_retriever(
    search_type="similarity", # 'similarity' is faster than 'mmr'
    search_kwargs={'k': 3}     # Only send 2 parents to the AI
    
)

while True:
    # user_query = str(input("[User]: "))
    user_query = input("\n[User]: ").strip()    
    if user_query:
        if user_query.lower() in ['q','exit','quit']: break

        # decision_chain = promt_decide | model | parser
        # decision = decision_chain.invoke({'user_query':user_query})
        use_rag = any(word in user_query.lower() for word in RAG_KEYWORDS)
        not_use_rag = any(word in user_query.lower() for word in NOT_RAG_KEYWORDS)


        
        if use_rag:
            print("Retrieve information from PDF")
            context = multi_query_generator(user_query,model,base_retriever)
            chain = prompt | model | parser


        elif not_use_rag:
            context = "Answer like human"
            chain = promt_general | model | parser
        else:
            context = "Answer like human"
            chain = promt_general | model | parser

        print("[L.I.G.H.T]: ", end="", flush=True)
        for chunk in chain.stream({'context':context,'user_query':user_query}):
                print(chunk,end="",flush=True)

        print('\n')

            



