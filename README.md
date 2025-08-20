# RAG Hukum Indonesia — UUD & UU (LangChain + Chroma + Gemini)

Aplikasi RAG untuk menanyakan isi **UUD 1945** dan beberapa **Undang-Undang** (sumber: **BPK Peraturan**).

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

1. Masuk ke folder `src/`
2. Buat file `.env` dari template:
   ```bash
   cp .env.example .env
   # isi GOOGLE_API_KEY di .env
3. Jalankan:
    ```bash
    docker compose up --build

4. Buka browser: http://localhost:8501
5. Ajukan pertanyaan di chat
