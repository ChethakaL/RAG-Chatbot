import os, mimetypes
import gradio as gr
from gpt4all import GPT4All
from doc_parser import parse_file
from embedder import create_embeddings, build_faiss_index
from rag_pipeline import get_top_k_chunks, generate_prompt

chunks, faiss_index, file_uploaded = [], None, False
model = GPT4All("Phi-3-mini-4k-instruct.Q4_0.gguf")


def handle_file_upload(file_path: str):
    global chunks, faiss_index, file_uploaded

    if not file_path:
        return "❌ No file selected."

    # Limit file size (demo constraint)
    if os.path.getsize(file_path) > 1_500_000:  # ~1.5 MB
        return "⚠️ File too large for demo. Please upload something smaller."

    mime, _ = mimetypes.guess_type(file_path)
    if mime not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "application/msword"]:
        return f"⚠️ Unsupported: {mime or 'unknown'}"

    text = parse_file(file_path)

    # Fewer larger chunks
    chunks = [text[i:i + 800] for i in range(0, len(text), 800)]
    faiss_index = build_faiss_index(create_embeddings(chunks))
    file_uploaded = True

    return f"✅ Processed **{os.path.basename(file_path)}** – ask away!"


def chat_with_doc(message, history):
    if not file_uploaded:
        return "⚠️ Please upload a document first.", history

    top_chunks = get_top_k_chunks(message, chunks, faiss_index, k=3)
    prompt = generate_prompt(top_chunks, message)

    if len(prompt) > 3500:
        prompt = prompt[:3500] + "\n\n[Truncated for length]"

    try:
        answer = model.generate(prompt, max_tokens=200, temp=0.2)
    except Exception as e:
        answer = f"❌ Model error: {str(e)}"

    # ⬇️ Return in Gradio's expected format: list of dicts
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})
    return "", history


with gr.Blocks(theme=gr.themes.Soft(), css="""
#chat-wrapper {
    height: 85vh;
    display: flex;
    flex-direction: column;
}

#chat-area {
    flex: 1;
    overflow-y: auto;
}

#input-area {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
    gap: 8px;
    background: #1c1c1e;
}

#input-area button {
    align-self: center;
    justify-self: center;
}
""") as demo:
    gr.Markdown("## 🧠 Vertical RAG Chatbot — GPT4All")

    with gr.Row():
        with gr.Column(scale=1):
            uploader = gr.File(label="📁 Upload PDF or DOCX")
            upload_status = gr.Markdown()
            uploader.change(fn=handle_file_upload, inputs=uploader, outputs=upload_status)
            gr.Markdown("""
            ⚠️ **Demo Limitations**
            - Max file size: ~1.5 MB  
            - Response time: ~50–60 seconds (runs fully offline on CPU)  
            - Best for small documents or short queries  
            - AI model: [Phi-3 Mini 4K Instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) via GPT4All
            """)

        with gr.Column(scale=2):
            with gr.Column(elem_id="chat-wrapper"):
                chatbot = gr.Chatbot(type="messages", elem_id="chat-area")
                with gr.Row(elem_id="input-area"):
                    msg = gr.Textbox(placeholder="Type a message...", scale=8)
                    submit = gr.Button("Send", scale=1)
                msg.submit(chat_with_doc, [msg, chatbot], [msg, chatbot])
                submit.click(chat_with_doc, [msg, chatbot], [msg, chatbot])

    gr.Markdown("⚡ Optimized for fast demo | GPT4All + FAISS + sentence-transformers")

if __name__ == "__main__":
    demo.launch()
