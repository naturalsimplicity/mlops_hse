FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir -U pip

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY mlapp /app/mlapp

EXPOSE 8000
CMD ["uvicorn", "mlapp.server:app", "--host", "0.0.0.0", "--port", "8000"]
