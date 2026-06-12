import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv(find_dotenv())

DB_DIR = "./vector_vault"

# Cache the vector database connection to prevent lag on every rerun
@st.cache_resource
def load_vector_db():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(
        collection_name="neuro_textbook",
        embedding_function=embedding_model,
        persist_directory=DB_DIR
    )
    return vector_db

def main():
    # Page Configurations
    st.set_page_config(
        page_title="NeuroScience Explorer", 
        page_icon="🧠", 
        layout="centered"
    )
    
    # UI Header
    st.title("🧠 Neuroscience Explorer")
    st.caption("Ask questions about brain function, cellular mechanisms, and neurobiology.")
    st.divider()

    # Verify API Key Presence
    if not os.environ.get("GROQ_API_KEY"):
        st.error("❌ `GROQ_API_KEY` not found in environment variables. Please check your `.env` file.")
        return

    # Initialize Vector DB connection (cached)
    with st.spinner("Connecting to Knowledge Vault..."):
        try:
            vector_db = load_vector_db()
        except Exception as e:
            st.error(f"Failed to connect to Vector Vault: {e}")
            return

    # User Input Element
    query = st.text_input("🤔 Ask a neuroscience question:", placeholder="e.g., How does the hippocampus consolidate memory?")

    if query:
        if not query.strip():
            st.warning("Please enter a valid question.")
            return

        # 1. Retrieval Phase
        with st.spinner("Scanning textbook for relevant concepts..."):
            # Fetch top 3 chunks to give the LLM slightly more context
            docs = vector_db.similarity_search(query, k=3) 

        # 2. Display Sourced Context to the user (Expandable UI)
        st.subheader("📂 Retrieved Textbook Excerpts")
        for i, doc in enumerate(docs):
            with st.expander(f"Excerpt #{i+1}"):
                st.write(doc.page_content)

        # 3. Compile Master Prompt for pure Neuroscience Q&A
        prompt_1 = [
            ("system", "You are an expert neuroscientist and biology specialist.\n"
                    "Your primary task is to answer the user's question using the provided textbook excerpts in the most easy and simple explanable way but be accurate.\n\n"
                    "Guidelines:\n"
                    "1. If the provided excerpts contain the answer, rely heavily on them and cite them implicitly.\n"
                    "2. If the excerpts do not contain sufficient data, do not refuse the question. Instead, clearly state: 'While the specific textbook excerpts do not cover this fully, based on general neurobiology...' and then provide an accurate scientific answer using your baseline knowledge.\n"
                    "3. Keep the explanation structured, academic, and Sukuna style."),
            ("human", f"Question: {query}\n\nContext:\n" + "\n\n".join([d.page_content for d in docs]) + "\n\nProvide the neuroscience answer.")
        ]

        # 4. Inference Phase
        with st.spinner("Synthesizing answer..."):
            try:
                llm = ChatGroq(model_name="llama-3.1-8b-instant")
                response = llm.invoke(prompt_1)
                
                # 5. Render Output cleanly
                st.divider()
                st.subheader("🔬 Scientific Explanation")
                st.markdown(response.content)
                
            except Exception as e:
                st.error(f"Inference Engine Error: {e}")

if __name__ == "__main__":
    main()