FROM python:3.11.4-slim

# Set working directory
WORKDIR /query

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "query.main:app", "--host", "0.0.0.0", "--port", "8000"]