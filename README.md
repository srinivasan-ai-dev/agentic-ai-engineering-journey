# 🚀 30 Days of Agentic AI Engineering

Welcome to my 30-day engineering journal. This repository documents my deep dive into building end-to-end Agentic AI systems, transitioning from foundational LLM calls to fully autonomous, multi-agent RAG architectures. 

This journey follows the advanced Agentic AI frameworks taught by Codebasics, focusing on hands-on deployment over pure theory.

## 📂 Project Architecture

This mono-repo contains a progression of increasingly complex AI applications:

### 1. Simple LLM Calling (`/1_simple_llm_calling`)
* The foundational setup for securely connecting to LLM APIs (Groq/Gemini).
* Establishes basic prompt engineering pipelines and environment variable management.

### 2. Multi-Modal Blood Work Analyzer (`/2_blood_work_analysis`)
* A full-stack AI application that processes medical reports.
* Generates structured 50-word medical summaries and culturally tailored Indian dietary plans.
* **Key Skills:** Streamlit UI, LangChain Prompts, Regex Output Parsing, Pydantic Structured Outputs.

### 3. 🧠 Neuroscience Explorer (RAG Pipeline)

**Live Demo:** (https://agentic-ai-engineering-journey.streamlit.app)

### Architecture Overview
This project is a Retrieval-Augmented Generation (RAG) pipeline designed to extract highly technical neurobiology data from unstructured text. 
* **Embedding Model:** `all-MiniLM-L6-v2` (HuggingFace) for dense vector representation.
* **Vector Store:** ChromaDB for semantic similarity search.
* **Inference Engine:** Llama-3.1-8b (via Groq API) for high-speed, low-latency generation.
* **Frontend:** Streamlit for the user interface.

### Guardrails Implemented

To balance strict data grounding with user helpfulness, the LLM utilizes a Hybrid Knowledge Architecture. The system prioritizes fetching exact excerpts from the embedded textbook vault to prevent biological hallucination. If a query falls outside the bounds of the retrieved text, the inference engine executes a graceful fallback—blending the available context with baseline neurobiological consensus to deliver a complete, scientifically accurate response.
---

## 🛠️ The Tech Stack

* **Core Language:** Python 3.x
* **AI Orchestration:** LangChain & LangChain-Groq
* **LLMs Used:** Groq (Qwen / Llama 3), Google Gemini
* **Databases:** ChromaDB (Vector), SQLite (Relational)
* **Frontend UI:** Streamlit
* **Environment Management:** `python-dotenv`

---

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/srinivasan-ai-dev/agentic-ai-engineering-journey.git](https://github.com/srinivasan-ai-dev/agentic-ai-engineering-journey.git)
   cd agentic-ai-engineering-journey
