#!/usr/bin/env python3
# mypy: strict
"""
Streamlit RAG App for Indonesian Legal Documents (UUD 1945 & several UUs)

Tech stack:
- LangChain (RAG pipeline)
- ChromaDB (vector store, persisted)
- FastEmbed (free embeddings)
- Gemini (LLM via Google Generative AI)
- Streamlit (chat UI)
- Production-minded: mypy type hints, ruff-compliant

How to run:
- Local: `streamlit run app.py`
- Docker: `docker compose up --build` (from src/)

Author: Fahri Alfiansyah
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import List

import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate


# ========== CONFIG ==========
load_dotenv()  # Load environment variables from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY tidak ditemukan. Pastikan Anda sudah membuat file .env.")

# Dapatkan direktori tempat script ini berada
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"  # Folder untuk menyimpan database vektor


# ========== LOAD PDF DOCUMENTS ==========
PDF_FILES = [
    DATA_DIR / "UUD45_SatuNaskah.pdf",
    DATA_DIR / "UU Nomor 6 Tahun 2023.pdf",
    DATA_DIR / "UU Nomor 30 Tahun 2002.pdf",
    DATA_DIR / "UU Nomor 3 Tahun 2025.pdf",
]

def load_documents() -> List:
    """Load all PDF documents from ./data folder"""
    docs = []
    for file_path in PDF_FILES:
        if not file_path.exists():
            raise FileNotFoundError(f"❌ File tidak ditemukan: {file_path}")
        loader = PyPDFLoader(str(file_path))
        docs.extend(loader.load())
    return docs


# ========== CREATE VECTORSTORE ==========
def create_vectorstore():
    """Split docs, embed, and store in ChromaDB"""
    docs = load_documents()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    splits = text_splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print(f"📄 Jumlah dokumen hasil split: {len(splits)}")
    vectordb = Chroma.from_documents(splits, embeddings, persist_directory=str(CHROMA_DB_DIR))
    vectordb.persist()
    return vectordb


# ========== LOAD VECTORSTORE ==========
def get_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    if CHROMA_DB_DIR.exists():
        return Chroma(persist_directory=str(CHROMA_DB_DIR), embedding_function=embeddings)
    else:
        return create_vectorstore()


# ========== RAG PIPELINE ==========
def rag_answer(question: str) -> str:
    vectordb = get_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    # Retrieve relevant docs
    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])

    # LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=GOOGLE_API_KEY)

    # Prompt Engineering
    prompt_template = ChatPromptTemplate.from_template(
        """
        Anda adalah asisten AI hukum yang ahli dalam hukum Indonesia.
        Jawablah pertanyaan pengguna dengan mengacu pada dokumen hukum berikut.
        Berikan jawaban yang akurat, jelas, dan mengutip pasal/ayat yang relevan jika ada.

        Konteks dari dokumen hukum:
        {context}

        Pertanyaan pengguna:
        {question}

        Jawaban yang jelas, ringkas, dan relevan dengan mengutip dasar hukum yang sesuai:
        """
    )

    prompt = prompt_template.format(context=context, question=question)
    response = llm.invoke(prompt)
    return response.content


# ========== STREAMLIT UI ==========
def main():
    st.set_page_config(page_title="RAG Legal Assistant", layout="wide")
    st.title("📘 RAG Legal Assistant")
    st.write("Ajukan pertanyaan terkait **UUD 1945** atau **UU Indonesia** (dokumen di bawah).")

    # Menampilkan daftar dokumen yang dimuat
    with st.expander("📄 Dokumen yang Dimuat", expanded=True):
        for file_path in PDF_FILES:
            file_name = file_path.name
            if file_path.exists():
                st.markdown(f"- ✅ `{file_name}`")
            else:
                st.markdown(f"- ❌ `{file_name}`")

    # Input pertanyaan
    user_question = st.text_input("Masukkan pertanyaan Anda:")
    if st.button("Cari Jawaban") and user_question.strip():
        with st.spinner("🔎 Sedang mencari jawaban..."):
            try:
                answer = rag_answer(user_question)
                st.subheader("Jawaban:")
                st.write(answer)
            except FileNotFoundError as e:
                st.error(f"Error: {e}")
                st.error("Pastikan semua file PDF ada di folder data/")
            except Exception as e:
                st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
