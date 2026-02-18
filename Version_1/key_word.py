RAG_KEYWORDS = [
    # Explicit Source Mentions
    'from paper', 'from document', 'from pdf', 'from knowledge base',
    'in the paper', 'according to context', 'the text states','from context'
    
    
    # Action-Oriented
    'summarize the document', 'key findings', 'conclusion of the paper','summarize the pdf','summarize this pdf',
    'summarize this document','summarize this pdf'
]

NOT_RAG_KEYWORDS = [
    'do not use context','do not use pdf','without pdf','without document','without paper'
]