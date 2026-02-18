# L.I.G.H.T. (Logical Intelligence for Guidance, Help, and Tasks)

**Developed by:** [Mr. Leo (Darshan)]

L.I.G.H.T. is an advanced AI Assistant designed to bridge the gap between static documents and actionable intelligence. Built on the LangChain ecosystem, it serves as a grounded, conversational partner capable of deep document analysis and persistent memory.

---

## Core Capabilities

### 1. Semantic Document Intelligence (RAG)

L.I.G.H.T. doesn't just read; it understands.

- **Multi-Format Support:** Seamlessly ingest and analyze `.pdf` and `.txt` files.
- **Parent-Document Retrieval:** Uses advanced chunking strategies to ensure the AI sees the full context of a rule or regulation, not just a snippet.
- **Source Citations:** Every answer derived from a document includes specific references to sections or page numbers.

### 2. Cognitive Memory Architecture

Unlike standard chatbots, L.I.G.H.T. features a dual-layer memory system:

- **Short-Term Context:** Maintains the immediate "flow" of conversation.
- **Long-Term Persistence:** Remembers user preferences and past interactions across different sessions using a local vector database.

### 3. Humanized Reasoning

L.I.G.H.T. is programmed to prioritize clarity and empathy. It translates complex technical or legal jargon from documents into "human-friendly" explanations without losing accuracy.

---

## 🛠️ The Tech Stack

- **Orchestration:** [LangChain](https://www.langchain.com/) & [LangGraph](https://www.langchain.com/langgraph) (for complex stateful workflows).
- **Interface:** [Chainlit](https://chainlit.io/) (providing a sleek, ChatGPT-like UI).
- **Local LLM:** Powered by [Ollama](https://ollama.com/) (Qwen 2.5 3B / Nomic-Embed).
- **Vector Store:** [ChromaDB](https://www.trychroma.com/) for high-speed document indexing.

---

## Future Roadmap & Additional Features

### 🔹 1. Self-Correction Loop (Agentic RAG)

Using **LangGraph**, L.I.G.H.T. will verify its own answers. If the retrieved context doesn't answer the user's question, the AI will automatically re-phrase the search query and try again.

### 🔹 2. Vision Integration (OCR+)

Expand analysis to include images within PDFs and hand-written notes, allowing L.I.G.H.T. to interpret diagrams, charts, and tables.

### 🔹 3. "Audit Mode" (Actionable Tasks)

A specialized mode for Legal & HR compliance where the AI can generate a summary report of "missing requirements" based on a provided document.

### 🔹 4. Secure Local Execution

100% Privacy. All data processing and model inference happen locally on the user's hardware. No data ever leaves the machine.


# Note

***Idea and plan can update in future***
