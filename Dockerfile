FROM python:3.12.7
# Stage 1: Build stage to handle heavy ML/Data dependencies
FROM python:3.10-slim AS builder

WORKDIR /workspace

# Install system dependencies required for C-extensions (scipy, numpy, scikit-learn)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker caching layers
COPY requirements.txt .

# Remove '-e .' from requirements if it exists to avoid dependency loops during building,
# and explicitly install production-grade server tooling (uvicorn)
RUN sed -i '/-e ./d' requirements.txt && \
    pip install --no-cache-dir --user -r requirements.txt && \
    pip install --no-cache-dir --user uvicorn[standard]

# Stage 2: Clean, minimal runtime execution stage
FROM python:3.10-slim AS runner

WORKDIR /workspace

# Copy installed packages from the builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Copy the entire project code into the container execution workspace
COPY . .

# Install your local package 'networksecurity' in editable/local mode using setup.py
RUN pip install -e .

# Expose the default port for FastAPI
EXPOSE 8000

# Run Uvicorn pointing directly to app.py's internal app object instance
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]