# Step to run PDF RAG
1. Make dir `.streamlit` and make file `secret.toml`
    ```
    [general]
    OPENAI_API_KEY="sk-proj--
    ```
2. Make file `.env`
    ```
    OPENAI_API_KEY=sk-proj--
    LANGCHAIN_API_KEY=lsv2_pt_1754a762
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_PROJECT=pdf-rag-streamlit
   ```
   
3. Run the app
    ```
    streamlit run pdf_rag_ui.py
    ```
