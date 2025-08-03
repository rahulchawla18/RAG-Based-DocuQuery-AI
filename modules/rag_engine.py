import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st
from modules.model_selector import SimpleModelSelector

load_dotenv()

class SimpleRAGSystem:
    def __init__(self, embedding_model="openai", llm_model="openai"):
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.db = chromadb.PersistentClient(path="./chroma_db")
        self.setup_embedding_function()
        self.llm = (
            OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            if llm_model == "openai"
            else OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        )
        self.collection = self.setup_collection()

    def setup_embedding_function(self):
        try:
            if self.embedding_model == "openai":
                self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    model_name="text-embedding-3-small",
                )
            elif self.embedding_model == "nomic":
                self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
                    api_key="ollama",
                    api_base="http://localhost:11434/v1",
                    model_name="nomic-embed-text",
                )
            else:
                self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        except Exception as e:
            st.error(f"Embedding setup failed: {str(e)}")
            raise e

    def setup_collection(self):
        collection_name = f"documents_{self.embedding_model}"
        try:
            return self.db.get_collection(name=collection_name, embedding_function=self.embedding_fn)
        except:
            return self.db.create_collection(name=collection_name, embedding_function=self.embedding_fn)

    def add_documents(self, chunks):
        try:
            self.collection.add(
                ids=[chunk["id"] for chunk in chunks],
                documents=[chunk["text"] for chunk in chunks],
                metadatas=[chunk["metadata"] for chunk in chunks],
            )
            return True
        except Exception as e:
            st.error(f"Add doc error: {str(e)}")
            return False

    def query_documents(self, query, n_results=3):
        try:
            return self.collection.query(query_texts=[query], n_results=n_results)
        except Exception as e:
            st.error(f"Query error: {str(e)}")
            return None

    def generate_response(self, query, context):
        try:
            prompt = f"""
            Based on the following context, answer the question. If unsure, say "I don't know".
            Context: {context}
            Question: {query}
            Answer:
            """
            response = self.llm.chat.completions.create(
                model="gpt-4o-mini" if self.llm_model == "openai" else "llama3.2",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"LLM generation failed: {str(e)}")
            return None

    def get_embedding_info(self):
        model_selector = SimpleModelSelector()
        return model_selector.embedding_models[self.embedding_model]