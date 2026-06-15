FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies with optimizations
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy source code and models
COPY api/ ./api/
COPY src/ ./src/
COPY models/ ./models/

# Generate data and train model
RUN python src/preparar_datos.py && \
    python src/entrenar_modelo.py && \
    python src/evaluar_modelo.py

# Expose port 8080 (variación técnica)
EXPOSE 8080

# Health check for better container monitoring
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]