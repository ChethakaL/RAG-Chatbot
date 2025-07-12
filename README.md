# 🧠 Vertical RAG Chatbot — PDF Q&A with GPT4All

A simple and private Retrieval-Augmented Generation (RAG) chatbot that lets you upload a PDF or Word document and ask questions about its contents — all processed locally using open-source models.

![Screenshot](./screenshot.png) <!-- Replace with actual image if hosting -->

---

## ✨ Features

- 📁 Upload your own PDF or DOCX files
- 💬 Ask natural-language questions about the document
- 🔍 Uses **FAISS** for fast document chunk retrieval
- 🧠 Powered by **GPT4All + Phi-3 Mini** (offline local LLM)
- 🗂️ File parsing with `pdfplumber` and `python-docx`
- 🧩 Embedding via `sentence-transformers`
- 🛜 Fully local — **no internet required for inference**

---

## ⚙️ Demo Limitations (Free CPU version)

- ⛔ Max file size: **~1.5 MB**
- 🐌 Response time: **~50–60 seconds**
- 🧠 Model: `Phi-3-mini-4k-instruct.Q4_0.gguf` via GPT4All (CPU only)
- 📄 No persistent storage (temporary session only)

> 💡 For faster results or larger documents, you can switch to **OpenAI GPT-3.5** or host on a GPU.

---

## 🚀 Quick Start (Local)

1. **Clone this repo**
   ```bash
   git clone https://github.com/yourname/vertical-rag-chatbot.git
   cd vertical-rag-chatbot
