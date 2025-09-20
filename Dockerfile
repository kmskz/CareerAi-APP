# Use official Python image
FROM python:3.11-slim

WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose port
EXPOSE 8080

# Run Streamlit in headless mode
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]



