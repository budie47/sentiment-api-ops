# 1. Start with a lightweight Linux environment that has Python 3.11 pre-installed
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements first (this is a caching trick to make rebuilds faster)
COPY requirements.txt .

# 4. Install the heavy AI libraries (this will take a few minutes during the build)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your actual application code
COPY main.py .

# 6. Expose the port so traffic can reach the API
EXPOSE 8000

# 7. The command that runs when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]