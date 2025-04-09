# SHL Assessment Search System

A semantic search system for SHL assessments with metadata filtering capabilities, featuring a FastAPI backend and Streamlit frontend.

## Overview

This project provides a complete solution for searching and filtering SHL assessments using natural language queries. The system scrapes assessment data from SHL's product catalog, processes it using advanced NLP techniques, and makes it searchable through both an API and a user-friendly web interface.

## Features

- **Semantic Search**: Find assessments based on natural language queries
- **Metadata Filtering**: Filter by job level, language, duration, test type, remote support, adaptive support
- **Intelligent Query Understanding**: Extract implied filters from natural language queries
- **User-Friendly Interface**: Easy-to-use Streamlit frontend
- **Robust API**: Flexible FastAPI backend for integration with other systems

## System Architecture

### 1. Data Collection

- Web scraper built with Selenium to extract assessment data from SHL's product catalog
- Collects assessment titles, descriptions, job levels, languages, and durations
- Saves data in both CSV and JSON formats

### 2. Data Ingestion Pipeline

- Processes raw data and creates searchable embeddings
- Uses LLM (Mixtral-8x7b-32768) to normalize metadata fields
- Generates vector embeddings using Sentence Transformers
- Stores data in Qdrant vector database via LlamaIndex

### 3. Search API (FastAPI)

- `POST /recommend`: Advanced query endpoint with structured request body

- Extracts implied filters from user queries using LLM

### 4. Frontend (Streamlit)

- User-friendly interface for searching assessments
- Displays search results with relevant metadata

## Getting Started

### Prerequisites

- Python 3.8+
- Chrome browser (for Selenium scraper)
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shl-assessment-search.git

```

2. Install dependencies:
```bash
cd Backend
pip install -r requirements.txt
cd Client
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file
QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=
GROQ_API_KEY=
LLM_MODEL_NAME=
EMBEDDING_MODEL_NAME=
TOP_K=
```

### Data Collection

Run the scraper to collect assessment data:
```bash
cd Backend
python scrape.py
```

### Data Ingestion

Process and index the collected data:
```bash
cd Backend
python ./Ingestion/ingestion_pipeline.py
```

### Running the Backend

Start the FastAPI server:
```bash
cd Backend
uvicorn query.main:app --host 0.0.0.0 --port 8000
```

### Running the Frontend

Start the Streamlit app:
```bash
cd Client
streamlit run main.py
```

## API Documentation

Once the backend is running, you can access the API documentation at:
```
http://localhost:8000/docs
```

### Key Endpoints

- `POST /query`: Main query endpoint with full filtering capabilities


## Deployment

### Docker

Build and run with Docker for both Backend and Client:
```bash
# Build images
docker-compose build

# Run services
docker-compose up -d
```

### Cloud Deployment

The system can be deployed to various cloud platforms:
- Backend: AWS Lambda, Google Cloud Run, Azure Functions
- Vector Database: Managed Qdrant service or self-hosted
- Frontend: Streamlit Cloud or any static hosting service

## Technical Stack

- **Web Scraping**: Selenium, Python
- **Vector Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database**: Qdrant
- **LLM Integration**: Groq API (Mixtral model)
- **Search Framework**: LlamaIndex
- **API Framework**: FastAPI with Pydantic models
- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy

## License

[MIT License](LICENSE)

## Acknowledgements

- [SHL](https://www.shl.com/) for providing the assessment catalog
- [LlamaIndex](https://www.llamaindex.ai/) for vector search capabilities
- [Groq](https://groq.com/) for LLM API access