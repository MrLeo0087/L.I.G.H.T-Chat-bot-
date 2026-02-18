import chainlit as cl
import sys, gc
from pathlib import Path
from pdf_reader_ui import database_action

# Ensure your custom modules are importable
sys.path.append(str(Path(__file__).parent.parent))
from model import embedding, model, parser
from promt import promt_general,prompt
from key_word import RAG_KEYWORDS
from supportive_function import multi_query_generator

async def pdf_preprocess(filepath):
    # Simply clear the old session variables
    cl.user_session.set('retriever', None)
    cl.user_session.set('vectorstore', None)
    
    # Get (or create) the specific database for this file
    vector_db = await database_action(filepath, embedding)

    retriever = vector_db.as_retriever(
        search_type="similarity", # 'similarity' is faster than 'mmr'
        search_kwargs={'k': 3})
    # retriever = vector_db.as_retriever(
    #     search_type='mmr', 
    #     search_kwargs={'k': 4, 'fetch_k': 10}
    # )
    
    cl.user_session.set('retriever', retriever)
    cl.user_session.set('vectorstore', vector_db)
    return vector_db

@cl.on_message
async def main(message: cl.Message):
    # Check for PDF uploads
    if message.elements:
        pdf_files = [el for el in message.elements if "pdf" in el.mime]
        if pdf_files:
            await pdf_preprocess(pdf_files[0].path)
            await cl.Message(content=f"✅ **{pdf_files[0].name}** is processed and ready!").send()
            return
        
    user_query = message.content
    retriever = cl.user_session.get('retriever')

    # Logic to determine if we use RAG or General Chat
    is_doc_query = any(word in user_query.lower() for word in RAG_KEYWORDS)
    
    if is_doc_query and retriever:
        async with cl.Step(name="Retrieving Context") as step:
            print("Retrieve information from PDF")
            context = multi_query_generator(user_query,model,retriever)
            selected_chain = prompt | model | parser
    else:
        context = ""
        selected_chain = promt_general | model | parser

    # Stream the response
    msg = cl.Message(content="")
    async for chunk in selected_chain.astream({'context': context, 'user_query': user_query}):
        await msg.stream_token(chunk)
    await msg.send()