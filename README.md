# Student Teacher Agent

A Python-based student-teacher assistant that can answer questions using an NVIDIA-hosted LLM, route simple calculations to a calculator tool, run web searches, remember chat history, and answer questions from a PDF using a small RAG pipeline.

## Features

- Student/teacher agent flow for interactive Q&A
- NVIDIA LLM integration through the OpenAI-compatible client
- Conversation memory saved in `data/chat_history.json`
- Calculator routing for basic math expressions
- Web search routing with `ddgs`
- PDF RAG chat using:
  - `pypdf` for PDF text extraction
  - `langchain-text-splitters` for chunking
  - `sentence-transformers` for embeddings
  - `faiss-cpu` for vector search

## Project Structure

```text
student_teacher_agent/
+-- agents/
|   +-- student_agent.py      # Student interface
|   +-- teacher_agent.py      # Main teacher logic
|   +-- router.py             # Routes calculator/search/LLM questions
+-- data/
|   +-- chat_history.json     # Saved conversation history
+-- llm/
|   +-- nvidia_client.py      # NVIDIA API client
+-- memory/
|   +-- memory.py             # JSON-based chat memory
+-- rag/
|   +-- pdf_reader.py         # Reads PDF text
|   +-- chunker.py            # Splits text into chunks
|   +-- embedding_model.py    # Creates embeddings
|   +-- vector_store.py       # FAISS vector index
|   +-- retriever.py          # Retrieves relevant chunks
|   +-- rag_chat.py           # PDF question-answering bot
+-- tools/
|   +-- calculator_tool.py    # Calculator tool
|   +-- search_tool.py        # Web search tool
+-- config.py                 # Loads environment variables
+-- main.py                   # Main student-teacher chat app
+-- requirements.txt          # Python dependencies
+-- sample.pdf                # PDF used by the RAG bot
```

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
NVIDIA_API_KEY=your_nvidia_api_key_here
```

## Run The Student Teacher Agent

```bash
python main.py
```

Example usage:

```text
=== Student Teacher Agent ===

You: What is artificial intelligence?
Teacher: ...

You: 12 * 8
Teacher: Answer = 96

You: search latest Python news
Teacher: ...
```

Type `exit` to stop the chat.

## Run The PDF RAG Chat

The RAG bot reads `sample.pdf`, creates chunks, builds embeddings, stores them in FAISS, and answers only from the retrieved PDF context.

```bash
python rag/test_rag.py
```

Example:

```text
Ask: What is this PDF about?
Answer:
...
```

Type `exit` to stop the RAG chat.

## How It Works

### Agent Chat

1. `main.py` accepts user input.
2. `StudentAgent` sends the question to `TeacherAgent`.
3. `Router` decides the route:
   - Math operators like `+`, `-`, `*`, `/` use the calculator.
   - Questions containing `search` use web search.
   - Everything else goes to the NVIDIA LLM.
4. `Memory` saves student and teacher messages in `data/chat_history.json`.

### PDF RAG

1. `read_pdf()` extracts text from `sample.pdf`.
2. `create_chunks()` splits the text into overlapping chunks.
3. `create_embeddings()` converts chunks into vectors.
4. `VectorStore` stores vectors in a FAISS index.
5. `Retriever` finds the most relevant chunks for a question.
6. `RAGChat` sends the retrieved context to the NVIDIA LLM and asks it to answer only from the PDF.

## Useful Test Files

You can run individual test scripts while developing:

```bash
python rag/test_pdf.py
python rag/test_chunks.py
python rag/test_embeddings.py
python rag/test_faiss.py
python rag/test_retriever.py
python rag/test_rag.py
```

API checks:

```bash
python test_nvidia.py
python test_nvidia_key.py
```

## Notes

- `sample.pdf` is currently hardcoded in `rag/rag_chat.py`.
- The first RAG run can take time because the embedding model is downloaded/loaded.
- Web search requires internet access.
- LLM answers require a valid `NVIDIA_API_KEY`.
- Chat memory is stored locally in `data/chat_history.json`.

## Troubleshooting

- If the NVIDIA request fails, check that `.env` exists and `NVIDIA_API_KEY` is valid.
- If PDF answers are empty, confirm that `sample.pdf` contains selectable text.
- If FAISS or sentence-transformer installation fails, upgrade pip first:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
