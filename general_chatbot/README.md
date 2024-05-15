# BlueBot🤖: Your {Domain_Specific} AI Chat Mate

This repository contains the code for BlueBot, an AI-powered chatbot built with Streamlit, Claude-3, and ChromaDB. BlueBot is designed to answer your questions about any document you upload, providing a convenient and efficient way to access information. 

## Warning

🚧 Under Construction: Experimental Project 🚧
This project is a fun exploration of LLMs and RAG pipelines.

Please note: This is a work in progress and considered experimental. While we aim to provide a fun learning experience, the project is still under development and may have limitations or bugs. We welcome your feedback and contributions as we continue building this project.

## Features

* **Natural Language Interaction:** BlueBot understands natural language queries and provides comprehensive answers.
* **PDF Document Processing:**  BlueBot can process PDF documents and extract relevant information.
* **RAG (Retrieval-Augmented Generation):**  BlueBot leverages RAG to retrieve relevant information from the PDF and summarize it in response to your questions.
* **Claude-3 Integration:**  BlueBot uses Claude-3, a powerful language model from Anthropic, for its reasoning and generation capabilities.
* **ChromaDB Integration:**  ChromaDB is used for efficient indexing and retrieval of information from the PDF document. 
* **Streamlit Interface:**  The chatbot features a user-friendly Streamlit interface for easy interaction. 

## How to Use

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   ```
   
2. **Navigate to the root directory:**
   ```bash
   cd <repository_name>
   ```
   
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Create an Anthropic API Key:**
   * Sign up for an Anthropic account at https://www.anthropic.com/.
   
   * Create an API key in your Anthropic dashboard.
   
   * Place your API key in a file named anthro_key.txt in the data folder.

5. **Run the Application:**
   ```bash
   streamlit run app/chatbot.py
   ```
   if you like to customize the app then use
   ```bash
   streamlit run app/chatbot.py --server.runOnSave=true
   ```

6. **Upload a PDF File:**
   * Click the "Choose a PDF file to get started" button and select your .pdf document.

7. **Ask Questions:**
   * Type your question in the chat box.
   * BlueBot will use the information in the PDF to answer your questions.

8. **Example Usage**
   * Upload an HR benefits document or FAQ document in PDF format.
   
   * Ask a question like: "What is the company's policy on paid time off?" or "Anything relevant to the info on the PDF document uploaded"
   
   * BlueBot will extract relevant information from the PDF and provide a summary answer.

9. **Customization**
   * Configuration: You can adjust settings such as the chunk size, maximum tokens, and temperature for the language model in the chatbot.py file.
   
   * Data Folder: The data folder is used to store uploaded files and the Anthropic API key. You can modify the path to this folder in the code.
   
   * Domain: The chatbot_domain variable can be customized to reflect the specific domain of the chatbot (e.g., "HR Benefits", "Company Policies").
   
   * Name: The chatbot_name variable can be customized to reflect the custom name of the chatbot

10. **Contributions**
    * Contributions are welcome! If you have any suggestions, improvements, or bug fixes, feel free to submit a pull request.

11. **License**
    * This project is licensed under the MIT License. See the LICENSE file for details.