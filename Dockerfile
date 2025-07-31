FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev && rm -rf /var/lib/apt/lists/*

# Copy backend files first
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt sse_starlette

# Copy entire project structure
COPY . .

# Create symlink to match ../frontend path
RUN ln -s /app/frontend /app/backend/../frontend

EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]