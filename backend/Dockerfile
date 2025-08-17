FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

EXPOSE 8000

# Command to fastapi server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]