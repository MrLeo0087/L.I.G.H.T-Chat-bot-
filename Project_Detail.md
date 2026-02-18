# L.I.G.H.T (**L**ogical **I**ntelligence for **G**uidance, **H**elp, and **T**asks)

 Input = Text

* Output = Text
* Process = Generate humanize text and reply
* Feature :

  * Normal Conversation
  * Basic Code
  * PDF, txt reader and analysis
* Tools:

  * Lang - Chain
  * ChainlitLimitation

# Feature

- Normal Conversation
- Simple code generator
- Simple PDF RAG implement

# Limitation

- No memory
- Not effective RAG
- Slow
- Can't work with website or youtube video links

# Rule

- I use ollama .. so first install ollama then pull **qwen2.5:3b** model
- For run chainlit app first **cd .\Chain_lit_UI\** then run chainlit run **app.py** command in terminal
- After upload pdf, if you ask any question .. you have to tell model that give answer **from pdf**.
  One of them word have to in your query :
  ***RAG_KEYWORDS= [**
  *

* 'from paper', 'from document', 'from pdf', 'from knowledge base',*
* 'in the paper', 'according to context', 'the text states','from context'*
* 'summarize the document', 'key findings', 'conclusion of the paper','summarize the pdf',*
* summarize 	this pdf',    'summarize this document','summarize this pdf'**]***

  **Because, i can't use decision model . it take time and make slow**

- The PDF RAG is very basic RAG. It's should not able to give perfect answer. so use carefully

**OVERALL, This is first version and it have so much problem .. i will improve in version 2**
