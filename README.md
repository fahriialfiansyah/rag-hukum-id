# RAG Hukum Indonesia — UUD & UU (LangChain + Chroma + Gemini)

Aplikasi RAG untuk menanyakan isi **UUD 1945** dan beberapa **Undang-Undang** (sumber: **BPK Peraturan**).
<img width="7684" height="4322" alt="localhost_8501_(Full HD)" src="https://github.com/user-attachments/assets/4bc4456c-5808-41c4-a32b-133ed1141697" />


## Fitur
- LangChain RAG (loader → splitter → FastEmbed → Chroma → retriever → prompt → Gemini)
- UI Streamlit dengan sitasi sumber (URL BPK)
- Persisten vector store (Chroma) di volume Docker
- Kualitas kode: mypy & ruff

## Sumber Dokumen
- UUD 1945 — https://peraturan.bpk.go.id/Details/101646/uud-no--
- UU No. 6 Tahun 2023 — https://peraturan.bpk.go.id/Details/246523/uu-no-6-tahun-2023
- UU No. 30 Tahun 2002 — https://peraturan.bpk.go.id/Details/44493/uu-no-30-tahun-2002
- UU No. 3 Tahun 2025 — https://peraturan.bpk.go.id/Details/319166/uu-no-3-tahun-2025

---

## Menjalankan via **Docker Compose** (Disarankan)

1. Clone Repositori & Masuk ke Direktori
   ```bash
   git clone https://github.com/fahriialfiansyah/rag-hukum-id.git
   cd rag-hukum-id/src
2. Buat File .env secara Manual:
   Buat file .env di folder src/ dengan isi seperti berikut:
   ```bash
   GOOGLE_API_KEY=masukkan_api_key_anda_di_sini

   # Opsional (override default)
   PERSIST_DIR=/app/chroma_db
   COLLECTION_NAME=bpk_hukum_id
   GOOGLE_GENAI_MODEL=gemini-2.5-flash
   ```
   Pastikan kamu sudah memiliki Google API Key dari [Google Generative AI](https://ai.google.dev/)
3. Jalankan Aplikasi:
    ```bash
    docker compose up --build

5. Buka browser: http://localhost:8501
6. Ajukan pertanyaan di chat
