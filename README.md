# 💊 AI Drug Information & Pricing Assistant

An end-to-end Hybrid RAG (Retrieval-Augmented Generation) application that combines pharmaceutical data retrieval with Large Language Models (LLMs) to provide accurate drug information, pricing details, manufacturer information, and intelligent medical insights.

## 🚀 Features

* Hybrid RAG Architecture
* ChromaDB Vector Database
* Ollama Local LLM Integration
* Drug Information Retrieval
* Exact SKU/Product Search
* Pharmaceutical Analytics Dashboard
* PDF Report Generation
* Query Logging & Monitoring
* Dataset Upload & Management
* MySQL Database Support
* Streamlit Interactive UI

---

## 🏗️ Architecture

```text
Drug Dataset (CSV)
        │
        ▼
   ingest.py
        │
        ▼
    ChromaDB
        │
        ▼
   retriever.py
        │
        ▼
     router.py
        │
 ┌──────┴──────┐
 │             │
Exact Search   RAG Search
 │             │
 ▼             ▼
Answer      Ollama LLM
 │             │
 └──────┬──────┘
        ▼
     Streamlit UI
        │
        ▼
      MySQL
```


## 🛠️ Technologies Used

### AI & Machine Learning

* LangChain
* Ollama
* Llama 3 / Qwen 2.5
* Sentence Transformers
* ChromaDB

### Backend

* Python
* MySQL

### Frontend

* Streamlit

### Data Processing

* Pandas
* NumPy

### Visualization

* Plotly

### Reporting

* ReportLab

---



## 👨‍💻 Author

**Rupam Sahu**

MCA (Artificial Intelligence)

Skills:
Python | Machine Learning | Deep Learning | Data Science | NLP | Computer Vision | Generative AI | RAG | LangChain



Give this repository a star and share it with others.
