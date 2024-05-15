import streamlit as st
import chromadb
import PyPDF2
import anthropic
import time
import os

# Global settings (adjust as needed)
from configs.config import CHUNK_SIZE, MAX_TOKENS, TEMPERATURE, chatbot_name, chatbot_domain

# Initialize ChromaDB
chroma_client = chromadb.Client()

# ---  Caching mechanism  ---
# Store collections and RAG results in memory 
collection_cache = {}
rag_cache = {}

def create_collections(file_name: str):
    trimmed_file_name = file_name.replace(" ", "")
    # """Creates or retrieves a collection from ChromaDB, potentially from cache."""
    collection_name = f"{trimmed_file_name.lower()}_collection"

    # Check if collection exists in cache
    if collection_name in collection_cache:
        return collection_cache[collection_name]

    # Otherwise, create the collection
    collection = chroma_client.get_or_create_collection(name=collection_name)

    # Load PDF and chunk text
    filename = file_name

    text = ""
    with open(f'data/{file_name}', "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()

    chunks = chunk_text(text, CHUNK_SIZE)
    metas = [str(i) for i in range(len(chunks))]
    strings = [chunk.replace('\n', '') for chunk in chunks]

    # Use batch_add for improved performance
    collection.add(
        documents=strings,
        metadatas=None,
        ids=metas
    )

    # Store collection in cache
    collection_cache[collection_name] = collection
    return collection

def chunk_text(text, chunk_size):
    """Splits text into chunks of a specified size."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text) and not text[end].isspace():
            while end > start and not text[end].isspace():
                end -= 1
        chunks.append(text[start:end])
        start = end
    return chunks

def ask_rag(query: str, file_name):
    trimmed_file_name = file_name.replace(" ", "")
    # """Performs RAG query, potentially using cached results."""
    query_key = f"{trimmed_file_name}_{query}"  # Cache key for this query
    
    # Check for cached response
    if query_key in rag_cache:
        return rag_cache[query_key]
    
    collection = create_collections(file_name)
    results = collection.query(
        query_texts=[query],
        n_results=20
    )

    data = results["documents"][0]
    
    with open('data/anthro_key.txt', 'r') as f:
        anthro = f.read()

    client = anthropic.Anthropic(api_key=anthro,)

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system="You are a RAG summary bot. Summarize the snippets.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Summarize this text in response to this question. question: {query} texts: {data}"
                    }
                ]
            }
        ],
    )

    response = message.content[0].text
    
    # Cache the RAG result
    rag_cache[query_key] = response
    return response

# --- Streamlit UI ---
st.title(f"I'm {chatbot_name} 🤖, your AI {chatbot_domain} Chat Mate 💬")
st.write("I'm an `AI Assistant` powered by `ClaudeAI-3-Opus` LLM and I can answer any of your questions regarding the document you upload!")

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go one directory up to reach the "data" folder
data_dir = os.path.join(current_dir, '..', 'data')

# Create the "data" folder if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

# Create a file uploader widget
uploaded_file = st.file_uploader("Choose a PDF file to get started.", type=["pdf"])

if uploaded_file is not None:
    # Check if the uploaded file is a PDF
    if uploaded_file.name.endswith(".pdf"):
        # Save the file to the "data" folder
        file_path = os.path.join(data_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        # st.success(f"File '{uploaded_file.name}' saved successfully to '{data_dir}'.")
    else:
        st.error("Please upload a PDF file.")

if uploaded_file:
    st.write(f'You uploaded: `{uploaded_file.name}`')
    st.write(f"Got a question for me about `{uploaded_file.name}`? I can help you! Type it in the chatbox below!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    prompt = st.chat_input(f"Hola 👋🏼. Got a question for me about `{uploaded_file.name}`? I can help you!")

    if prompt:
        start_time = time.time()  # Start timing
        prompt_msg = f"`User`: {prompt}"
        with st.chat_message("user"):
            st.markdown(prompt_msg)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response_prompt = ask_rag(prompt, uploaded_file.name)
        response = f"`AI-Bot`: {response_prompt}"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        end_time = time.time()  # Stop timing
        st.write(f"Processing time: {end_time - start_time:.2f} seconds")  # Display time
# else:
#     st.write("Choose an organization so that we can chat and I can help you!")

st.markdown(
    """
    <div style="text-align:center;">
        <p style="font-size:14px;">Created by Akhil Joseph, Data Scientist @ IBX </p>
        <p style="font-size:12px;">Created with Streamlit, Claude-AI, ChromaDB and 💙 </p>
    </div>
    """,
    unsafe_allow_html=True
)