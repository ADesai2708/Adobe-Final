FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the model inside Docker image
RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-MiniLM-L6-v2')"

# Run the persona extraction script
ENTRYPOINT ["python3", "src/run_persona.py"]
