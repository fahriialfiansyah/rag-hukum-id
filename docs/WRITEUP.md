# WRITEUP — RAG Hukum Indonesia

## 1. Arsitektur Solusi

**Komponen utama:**
- **Data Source:** Halaman peraturan di `peraturan.bpk.go.id` (UUD 1945, UU No.6/2023, UU No.30/2002, UU No.3/2025).
- **Loader:** `WebBaseLoader` (LangChain Community) untuk mengunduh HTML.
- **Chunking:** `RecursiveCharacterTextSplitter` (chunk_size=1200, overlap=150) agar pasal/ayat tidak terputus ekstrim.
- **Embeddings:** `FastEmbedEmbeddings` (gratis, cepat).
- **Vector Store:** **Chroma**, dipersistenkan ke folder/volume Docker.
- **Retriever:** Similarity search (top-k default 5).
- **Prompt Engineering:** System prompt mewajibkan rujukan dasar hukum, hindari halusinasi.
- **Generator:** **Gemini** via `langchain-google-genai` (`gemini-2.5-flash`).
- **UI:** **Streamlit** chat-style (Build Index, Clear Index, Query).
- **Containerization:** Dockerfile + docker-compose dengan volume untuk `chroma_db`, `.env` untuk rahasia.

### Alur Data (RAG)
1. **Ingest**: Unduh HTML → Split → Embedding → Simpan ke **Chroma**.
2. **Query**: Ambil top-k chunk relevan → Format konteks → Prompt Gemini → Jawab + tampilkan sumber.

## 2. Keputusan Desain

- **Chroma + FastEmbed**: Keduanya **gratis**, stabil, dan cepat untuk baseline.
- **Chunk 1200/150**: Trade-off coverage vs. fragmentasi. Uji empiris menunjukkan jawaban legal lebih stabil dgn chunk lebih besar.
- **Gemini `1.5-flash`**: Latency lebih rendah untuk UI interaktif; opsi `1.5-pro` tersedia di sidebar untuk jawaban lebih teliti.
- **Prompt**: Menekankan rujukan bagian/pasal dan kejujuran saat tidak menemukan informasi.
- **Sumber di UI**: Ditampilkan unik (dedup) agar mudah ditelusuri kembali.

## 3. Cara Kerja Kode (ringkas baris-per-baris penting)

- `AppConfig`: konfigurasi global (persist dir, model default, chunking).
- `get_embeddings()` & `get_vectorstore()`: cache resource Streamlit → inisialisasi **FastEmbed** dan **Chroma**.
- `build_or_update_index()`:
  - `load_documents()` → `split_documents()` → `vs.add_documents()` → `vs.persist()`.
- `make_rag_chain()`:
  - `retriever` (Chroma) → `ChatPromptTemplate` dgn `MessagesPlaceholder` → LLM (Gemini) → `StrOutputParser`.
- `run_rag_with_sources()`:
  - Jalankan retriever untuk menyimpan **dokumen sumber** (ditampilkan di UI).
  - Panggil chain untuk menghasilkan jawaban.
- **UI**:
  - Sidebar mengatur API Key, model, `top_k`, tombol Build/Clear.
  - Chat mengelola `st.session_state.messages`.

## 4. Evaluasi (Sesuai Kriteria)

- **Functionality**: 
  - RAG end-to-end berjalan.
  - Menampilkan sumber URL BPK untuk verifikasi.
- **Code Structure**:
  - Type hints (mypy strict).
  - Lulus ruff (PEP8).
  - Fungsi terpisah (ingestion, retrieval, chain).
- **Technology Usage**:
  - Streamlit UI, LangChain pipeline (LCEL), Chroma, FastEmbed, Gemini.
  - Siap ditingkatkan ke **LangGraph** bila perlu orkestrasi kompleks.
- **Development Practices**:
  - Siap untuk git (Makefile, pyproject untuk tooling).
  - `.env` untuk secrets.
- **Documentation**:
  - `docs/README.md` (runbook), `docs/WRITEUP.md` (penjelasan teknis).
- **Future Improvement**:
  - Lihat bagian di bawah.

## 5. Pengujian Manual (Contoh Prompt)
- *"Apa wewenang KPK menurut UU 30/2002?"*
- *"Bagaimana kedudukan UUD 1945 dalam hierarki?"*
- *"Apa perubahan penting pada UU No. 3 Tahun 2025?"*
- Verifikasi: Apakah jawaban menyertakan dasar hukum + sumber BPK.

## 6. Keamanan & Privasi
- **API Key** tidak pernah di-hardcode. Dibaca dari `.env` / environment / sidebar.
- Container menjalankan user non-root.
- Volume khusus untuk vector store (memudahkan rotasi/backup).

## 7. Peningkatan Mendatang
- **LangGraph**: Node-based graph (Condense Question → Retrieve → (Re-rank) → Generate → Cite Guard).
- **Re-ranker**: BGE reranker / Cohere Rerank untuk presisi konteks.
- **Schema-aware chunking**: Split berdasarkan heading/pasal/ayat via regex/HTML DOM.
- **Evaluation harness**: Judgement LLM + golden set Q/A untuk regression test.
- **Observability**: LangSmith / OpenTelemetry tracing.
- **Auth**: Protect UI dengan password / OAuth bila dipublikasikan.
- **PDF snapshot**: Simpan versi PDF untuk acuan stabil per pasal.
