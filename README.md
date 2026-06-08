# Student Teacher Agent

Student Teacher Agent is a Python-based AI learning assistant with a Streamlit UI, CLI mode, PDF/RAG support, web search, intent detection, answer formatting, confidence scoring, and multi-agent orchestration.

The project is designed like a teacher pipeline: the user asks a question, the system detects intent, routes the question to the right tool or agent, retrieves/searches when needed, reviews the result, formats it, and returns a polished answer.

## Features

- Streamlit chat interface in `app.py`
- CLI chat mode in `main.py`
- NVIDIA-compatible LLM client integration
- PDF question answering using RAG and FAISS
- Web search using DuckDuckGo/DDGS
- Tavily-powered advanced web search
- Query rewriting for better search quality
- Intent detection for exam, interview, comparison, research, short-answer, and general questions
- Search result summarization
- Multi-agent comparison flow using Search + RAG in parallel
- Multi-PDF RAG support from `uploads/pdfs`
- CrossEncoder reranking for better RAG chunk selection
- Formatter and answer generator for professional markdown output
- Confidence scoring
- Execution time monitoring
- Persistent chat memory and run logs

## Current Agent System

```text
agents/
|-- student_agent.py              # Student wrapper that asks the teacher
|-- teacher_agent.py              # Main entrypoint for answering questions
|-- supervisor_agent.py           # Orchestrates tool/agent execution
|-- router.py                     # Routes questions to search, rag, math, multi, or knowledge
|-- intent_agent.py               # Detects user intent
|-- planner_agent.py              # Plans multi-agent search/RAG queries
|-- query_rewriter_agent.py       # Rewrites ambiguous search queries
|-- search_agent.py               # Runs web search
|-- search_summarizer_agent.py    # Converts raw search results into structured news summaries
|-- rag_agent.py                  # Runs PDF/RAG answering
|-- combiner_agent.py             # Combines search and RAG results
|-- reflection_agent.py           # Creates comparison reports from evidence
|-- critic_agent.py               # Checks clarity without adding outside facts
|-- formatter_agent.py            # Formats answers professionally
|-- answer_generator_agent.py     # Final polished answer layer
|-- confidence_agent.py           # Scores answer confidence
|-- execution_monitor_agent.py    # Tracks execution time
|-- math_agent.py                 # Calculator flow
|-- memory_agent.py               # Memory helper agent
|-- research_agent.py             # Research helper
`-- registry.py                   # Agent registry/helper
```

## Project Structure

```text
student_teacher_agent/
|-- agents/                  # AI agents and orchestration logic
|-- data/                    # Stored chat data
|-- evaluation/              # Evaluation helpers
|-- llm/
|   `-- nvidia_client.py     # NVIDIA/OpenAI-compatible LLM client
|-- logs/
|   `-- agent_runs.jsonl     # Agent execution logs
|-- memory/
|   `-- memory.py            # JSON chat memory
|-- rag/
|   |-- chunker.py           # Text chunking
|   |-- embedding_model.py   # Embedding model loader
|   |-- pdf_reader.py        # PDF text extraction
|   |-- rag_chat.py          # RAG question answering
|   |-- retriever.py         # Chunk retrieval
|   `-- vector_store.py      # FAISS vector storage
|-- tools/
|   |-- calculator_tool.py   # Math tool
|   `-- search_tool.py       # Web search tool
|-- app.py                   # Streamlit app
|-- main.py                  # CLI app
|-- config.py                # Environment config
|-- requirements.txt         # Dependencies
|-- chunks.pkl               # Saved RAG chunks
|-- faiss_index.bin          # Saved FAISS index
`-- README.md
```

## Requirements

- Python 3.10+
- NVIDIA API key
- Dependencies from `requirements.txt`

Main packages:

- `streamlit`
- `openai`
- `python-dotenv`
- `pypdf`
- `sentence-transformers`
- `faiss-cpu`
- `langchain-text-splitters`
- `ddgs`

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
NVIDIA_API_KEY=your_nvidia_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Run

Streamlit UI:

```powershell
streamlit run app.py
```

CLI mode:

```powershell
python main.py
```

Exit CLI mode:

```text
exit
```

## How The Pipeline Works

### 1. Intent Detection

`IntentAgent` detects the style of answer needed:

```text
sql full form                         -> short_answer
python functions exam point of view   -> exam
python functions interview questions  -> interview
compare ...                           -> comparison
research ...                          -> research
default                               -> general
```

For `short_answer`, `TeacherAgent` directly returns a short answer format:

```markdown
# Topic

Full Form:
...

Meaning:
...

Use:
...
```

### 2. Routing

`Router` chooses the route:

```text
what is python                                      -> knowledge
latest ai news                                     -> search
latest python news                                 -> search
summarize chapter 1                                -> rag
compare python functions from pdf with latest news -> multi
10 + 20                                            -> calculator
```

### 3. Search Flow

For search questions:

```text
QueryRewriterAgent
-> 
SearchAgent
->
SearchSummarizerAgent
->
FormatterAgent
->
AnswerGeneratorAgent
->
ConfidenceAgent
->
ExecutionMonitor
```

Example query rewrite:

```text
latest python news -> latest python news programming language
latest ai news     -> latest ai news artificial intelligence
```

Expected search output:

```markdown
# Python News

## Top Updates

- Python ecosystem updates
- Community news
- Learning resources

## Key Insights

- Python remains actively developed
- New educational content is available

## Sources

- URL...
```

### 4. RAG Flow

For PDF/document questions:

```text
RAGAgent
->
RAGChat
->
Retriever
->
FAISS index
 ->
CrossEncoder reranker
->
FormatterAgent
->
AnswerGeneratorAgent
```

RAG uses saved chunks and FAISS index files:

```text
chunks.pkl
faiss_index.bin
uploads/pdfs/
```

When multiple PDFs exist in `uploads/pdfs`, their text is combined before chunking and indexing.

### 5. Multi-Agent Comparison Flow

For comparison questions involving PDF and latest/search content:

```text
PlannerAgent
->
SearchAgent + RAGAgent run in parallel
->
SearchSummarizerAgent
->
CombinerAgent
->
ReflectionAgent
->
CriticAgent
->
FormatterAgent
->
AnswerGeneratorAgent
->
ConfidenceAgent
->
ExecutionMonitor
```

Expected comparison format:

```markdown
# Comparison Report

## PDF Findings

## Search Findings

## Similarities

## Differences

## Final Conclusion
```

The comparison pipeline is evidence-preserving. It should not change topics, invent facts, or convert a PDF-vs-news comparison into an unrelated version comparison.

## Important Behavior

- Formatter must not invent information.
- Critic must not add outside facts.
- Search summarizer must not describe websites like "Python.org provides blogs".
- Search summarizer should summarize the search result pattern, such as ecosystem updates, community news, and learning resources.
- URLs should be preserved.
- Raw `SEARCH RESULT:` and `RAG RESULT:` dumps should not be shown in the final answer.
- For comparison answers, normal `Summary / Key Points / Detailed Explanation` format should not replace the comparison report format.

## Logs And Memory

Chat memory:

```text
chat_history.json
data/chat_history.json
```

Agent execution logs:

```text
logs/agent_runs.jsonl
```

Logged metadata can include:

- Query
- Route
- Agents used
- Execution time
- Confidence score
- Retrieved chunks status
- Timestamp

## Verification Commands

Compile important files:

```powershell
python -m py_compile main.py app.py
python -m py_compile agents\teacher_agent.py agents\supervisor_agent.py agents\router.py
python -m py_compile agents\intent_agent.py agents\formatter_agent.py agents\search_summarizer_agent.py
```

Run CLI tests:

```powershell
python main.py
```

Test 1:

```text
sql full form
```

Expected:

```text
INTENT: short_answer
```

Expected answer shape:

```markdown
# SQL

Full Form:
Structured Query Language

Meaning:
...

Use:
...
```

Test 2:

```text
latest python news
```

Expected:

```markdown
# Python News

## Top Updates

## Key Insights

## Sources
```

Test 3:

```text
compare python functions from pdf with latest python news
```

Expected:

```markdown
# Comparison Report

## PDF Findings

## Search Findings

## Similarities

## Differences

## Final Conclusion
```

Test 4:

```text
python functions exam point of view
```

Expected:

```text
INTENT: exam
```

Test 5:

```text
python functions interview questions
```

Expected:

```text
INTENT: interview
```

## Troubleshooting

If the app starts slowly:

- The embedding model may be loading.
- FAISS and saved chunks may be loading.
- Hugging Face may show an unauthenticated request warning. This is usually not fatal, but setting `HF_TOKEN` can improve rate limits.

If search gives unrelated Python snake results:

- Confirm `QueryRewriterAgent` is active.
- Console should show:

```text
SEARCH QUERY: latest python news programming language
```

If comparison output changes topic:

- Check `FormatterAgent`, `CriticAgent`, `ReflectionAgent`, and `AnswerGeneratorAgent` prompts.
- They must preserve PDF/Search topics and avoid outside facts.

If NVIDIA API fails:

- Check `.env`.
- Confirm `NVIDIA_API_KEY` is set.
- Confirm internet access is available.

If Tavily search fails:

- Check `.env`.
- Confirm `TAVILY_API_KEY` is set.
- Install `tavily-python` from `requirements.txt`.

If RAG answer is weak:

- Confirm `chunks.pkl` and `faiss_index.bin` exist.
- Confirm PDFs exist in `uploads/pdfs`.
- Rebuild the index after uploading new PDFs.
- Make sure at least one PDF contains the topic being asked.
- The reranker uses `BAAI/bge-reranker-base`, which may download on first run.

## Status

Current core components:

```text
Intent Agent          Working
Search Summarizer     Working
Router                Working
Planner               Working
Search                Working
RAG                   Working
Combiner              Working
Reflection            Working
Critic                Working
Formatter             Evidence-preserving
Query Rewriter        Working
Confidence            Working
Execution Monitor     Working
```

## License

This project is for learning and experimentation. Add a license file if you plan to publish or distribute it.
