# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Streamlit runs on port 8501
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "Dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]