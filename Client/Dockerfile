FROM python:3.11.4-slim

WORKDIR /app

COPY streamlit-requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]