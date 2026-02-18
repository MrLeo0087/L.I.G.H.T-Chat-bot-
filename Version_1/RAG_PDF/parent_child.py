import os, shutil, hashlib, json,uuid
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DB_PATH = "./pdf_embedding_database"
MANIFEST_FILE = os.path.join(DB_PATH,'manifest.json')

def database_action(filepath,embedding):
    hasher = hashlib.md5()
    with open(filepath,'rb') as f:
        hasher.update(f.read())
    current_hash = hasher.hexdigest()

    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE,'r') as f:
            stored_data = json.load(f)
            if stored_data.get('hash') == current_hash:
                    print(f"{os.path.basename(filepath)} is already in the database!")
                    # ADD collection_name HERE:
                    return Chroma(
                        persist_directory=DB_PATH, 
                        embedding_function=embedding, 
                        collection_name="PDF_Embedding"
                    )
                            
    print(f"Different File Detected. Wiping Database for: {os.path.basename(filepath)}")
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

    os.makedirs(DB_PATH, exist_ok=True)
    loader = PyPDFLoader(filepath)
    raw_docs = loader.load()

    p_splitter = RecursiveCharacterTextSplitter(chunk_size = 1300,chunk_overlap = 100)
    c_splitter = RecursiveCharacterTextSplitter(chunk_size = 300,chunk_overlap = 75)

    p_chunks = p_splitter.split_documents(raw_docs)

    final_Child_chunk = []
    for p in p_chunks:
        p_id = str(uuid.uuid4())
        c_chunks = c_splitter.split_documents([p])
        for c in c_chunks:
            c.metadata['p_id'] = p_id
            c.metadata['complete_context'] = p.page_content
            final_Child_chunk.append(c)

    vector_database = Chroma.from_documents(
        final_Child_chunk,
        embedding,
        persist_directory=DB_PATH,
        collection_name="PDF_Embedding"
    )

    with open(MANIFEST_FILE,'w') as f:
        json.dump({'filename':os.path.basename(filepath),'hash':current_hash},f)

    return vector_database




