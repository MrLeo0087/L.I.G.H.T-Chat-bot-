from promt import prompt_multi_query
from langchain_core.output_parsers import StrOutputParser

def multi_query_generator(query, llm, retriever):
    parser = StrOutputParser()
    chain = prompt_multi_query | llm | parser
    
    multi_queries = chain.invoke({'user_query':query})
    full_text = ""
    print('[Generated Queries]: ')
    for chunk in chain.stream({'user_query':query}):
        print(chunk,end="",flush=True)
        full_text +=chunk

    print('\n')

    multi_queries = [q.strip() for q in full_text.split('\n') if q.strip()]
    
    all_parent_contexts = []
    
    for q in multi_queries:
        if q.strip(): 
            docs = retriever.invoke(q)
            for doc in docs:
                parent_text = doc.metadata.get('complete_context', doc.page_content)
                all_parent_contexts.append(parent_text)

    unique_contexts = list(set(all_parent_contexts))
    print(f'Retrieve Information {len(unique_contexts)}')
    
    return "\n\n---\n\n".join(unique_contexts)




