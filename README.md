# 🧠 DocuQuery AI — PDF Question Answering with RAG

DocuQuery AI is a **Retrieval-Augmented Generation (RAG)** system built with **Streamlit**, allowing users to upload **PDF files**, process them into semantically meaningful chunks, and interactively query them using **OpenAI** or **Ollama** LLMs. The project leverages **ChromaDB** for vector storage and supports multiple **embedding models** and **LLMs** for flexible experimentation.

> _“Ask questions directly from your uploaded PDFs — like ChatGPT, but with your own documents.”_

## 🔧 Features

✅ Upload and parse PDF documents  
✅ Split documents into overlapping semantic chunks  
✅ Choose between multiple Embedding & LLM models  
✅ Store vector embeddings in ChromaDB  
✅ Query documents using natural language  
✅ Generate context-aware responses using RAG  
✅ Streamlit-based responsive UI

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/rahulchawla18/RAG-Based-DocuQuery-AI.git
cd RAG-BASED-DOCUQUERY-AI
```

### 2. Create a virtual environment

python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Set your environment variables

Create a .env file in the root:
    OPENAI_API_KEY=your-openai-api-key

If using Ollama locally for embeddings or LLMs, make sure Ollama is running.

### 5. Run the app

streamlit run app.py