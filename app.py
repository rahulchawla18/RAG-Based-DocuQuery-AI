import streamlit as st
from modules.model_selector import SimpleModelSelector
from modules.pdf_processor import SimplePDFProcessor
from modules.rag_engine import SimpleRAGSystem

st.set_page_config(page_title="RAG Document QA", layout="wide")

def main():
    st.title("📄🔍 Multi-File RAG Document QA")

    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()
    if "current_embedding_model" not in st.session_state:
        st.session_state.current_embedding_model = None
    if "rag_system" not in st.session_state:
        st.session_state.rag_system = None

    # Sidebar model selector
    model_selector = SimpleModelSelector()
    llm_model, embedding_model = model_selector.select_models()

    if embedding_model != st.session_state.current_embedding_model:
        st.session_state.processed_files.clear()
        st.session_state.current_embedding_model = embedding_model
        st.session_state.rag_system = None
        st.warning("Embedding model changed. Please re-upload your documents.")

    try:
        if st.session_state.rag_system is None:
            st.session_state.rag_system = SimpleRAGSystem(embedding_model, llm_model)

        embedding_info = st.session_state.rag_system.get_embedding_info()
        st.sidebar.info(
            f"Embedding Model:\n- Name: {embedding_info['name']}\n- Dimensions: {embedding_info['dimensions']}"
        )
    except Exception as e:
        st.error(f"Initialization Error: {str(e)}")
        return

    uploaded_files = st.file_uploader(
        "Upload PDF or Text files", type=["pdf", "txt"], accept_multiple_files=True
    )

    if uploaded_files:
        processor = SimplePDFProcessor()
        total = len(uploaded_files)
        progress = st.progress(0)

        for i, file in enumerate(uploaded_files):
            if file.name not in st.session_state.processed_files:
                with st.spinner(f"Processing {file.name}..."):
                    try:
                        if file.type == "application/pdf":
                            text = processor.read_pdf(file)
                        elif file.type == "text/plain":
                            text = file.read().decode("utf-8")
                        else:
                            st.warning(f"Unsupported file type: {file.name}")
                            continue

                        chunks = processor.create_chunks(text, file)

                        if st.session_state.rag_system.add_documents(chunks):
                            st.session_state.processed_files.add(file.name)
                            st.success(f"✅ Processed {file.name}")

                    except Exception as e:
                        st.error(f"❌ Error processing {file.name}: {str(e)}")

            progress.progress((i + 1) / total)

    if st.session_state.processed_files:
        st.markdown("---")
        st.subheader("🔍 Query Your Documents")
        query = st.text_input("Ask a question:")

        if query:
            with st.spinner("Generating response..."):
                results = st.session_state.rag_system.query_documents(query)
                if results and results["documents"]:
                    response = st.session_state.rag_system.generate_response(query, results["documents"][0])
                    if response:
                        st.markdown("### 📝 Answer:")
                        st.write(response)

                        with st.expander("View Source Passages"):
                            for i, doc in enumerate(results["documents"][0], 1):
                                st.markdown(f"**Passage {i}:**")
                                st.info(doc)
    else:
        st.info("👆 Upload PDF or text documents to get started!")

if __name__ == "__main__":
    main()