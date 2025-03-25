# Use a specific version for the base image
FROM python:3.12

# Set the working directory
WORKDIR /code

# Install libpq-dev for psycopg2
RUN apt-get update \
    && apt-get install -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Install FastAPI and Uvicorn
RUN pip install fastapi[all]==0.109.0 uvicorn==0.26.0

# Copy the application code
COPY ./app /code/app

# Create a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Expose the port (documentation purpose)
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
