import os, hashlib, json, uuid
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chainlit as cl

# Base directory for all your PDF databases
BASE_DB_DIR = os.path.abspath("./pdf_databases")

async def database_action(filepath, embedding):
    # 1. Create a unique ID based on the file content
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    file_hash = hasher.hexdigest()
    
    # Each PDF gets its own sub-folder
    pdf_db_path = os.path.join(BASE_DB_DIR, file_hash)
    os.makedirs(pdf_db_path, exist_ok=True)

    # 2. Check if this specific PDF has already been processed
    # We check for a 'chroma.sqlite3' file which indicates a finished DB
    if os.path.exists(os.path.join(pdf_db_path, "chroma.sqlite3")):
        async with cl.Step("Database Check") as step:
            step.output = f"✅ Found existing index for this file. Loading..."
            return Chroma(
                persist_directory=pdf_db_path, 
                embedding_function=embedding, 
                collection_name="PDF_Collection"
            )

    # 3. If not, process the PDF
    async with cl.Step("Processing New PDF") as step:
        loader = PyPDFLoader(filepath)
        raw_docs = loader.load()
        
        p_splitter = RecursiveCharacterTextSplitter(chunk_size=1300, chunk_overlap=100)
        c_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=75)
        
        p_chunks = p_splitter.split_documents(raw_docs)
        final_chunks = []

        for p in p_chunks:
            p_id = str(uuid.uuid4())
            c_chunks = c_splitter.split_documents([p])
            for c in c_chunks:
                c.metadata['p_id'] = p_id
                c.metadata['complete_context'] = p.page_content
                final_chunks.append(c)
        
        step.output = f"Extracted {len(final_chunks)} chunks."

    async with cl.Step("Vectorizing") as step:
        step.output = "Creating embeddings..."
        vector_db = Chroma.from_documents(
            documents=final_chunks,
            embedding=embedding,
            persist_directory=pdf_db_path,
            collection_name="PDF_Collection"
        )
        step.output = "✅ Done!"
        return vector_db