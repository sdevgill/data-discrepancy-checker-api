FROM python:3.12.3-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip

# Copy only the necessary files first
COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

# Define the entrypoint for the container
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
