FROM python:3.11-slim

WORKDIR /query

# Create a non-root user
RUN useradd -m -u 1000 user

# Set environment variables for cache locations
ENV HF_HOME=/query/.cache
ENV TRANSFORMERS_CACHE=/query/.cache/transformers
ENV SENTENCE_TRANSFORMERS_HOME=/query/.cache/sentence_transformers

COPY requirements.txt .

# Install dependencies with specific versions to support BAAI/bge-small-en-v1.5
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir transformers==4.34.0 sentence-transformers==2.2.2 huggingface_hub

# Create cache directories with proper permissions
RUN mkdir -p /query/.cache/huggingface/hub && \
    mkdir -p /query/.cache/transformers && \
    mkdir -p /query/.cache/sentence_transformers && \
    chown -R user:user /query/.cache

# Force huggingface to download the model config and weights
RUN python -c "from huggingface_hub import snapshot_download; snapshot_download('BAAI/bge-small-en-v1.5', cache_dir='/query/.cache/huggingface/hub')"

# Create a script to fix the model config
RUN echo 'import os, json\n\
model_path = "/query/.cache/huggingface/hub"\n\
for root, dirs, files in os.walk(model_path):\n\
    if "config.json" in files and "BAAI/bge-small-en-v1.5" in root:\n\
        config_path = os.path.join(root, "config.json")\n\
        print(f"Found config at {config_path}")\n\
        with open(config_path, "r") as f:\n\
            config = json.load(f)\n\
        if "model_type" not in config:\n\
            config["model_type"] = "bert"\n\
            with open(config_path, "w") as f:\n\
                json.dump(config, f, indent=2)\n\
            print(f"Updated {config_path} with model_type")\n'\
> /tmp/fix_config.py

# Run the script to fix the model config
RUN python /tmp/fix_config.py

COPY . .

# Make sure all files are accessible to the user
RUN chown -R user:user /query

# Switch to the non-root user
USER user

EXPOSE 7860

CMD ["uvicorn", "query.main:app", "--host", "0.0.0.0", "--port", "7860"]