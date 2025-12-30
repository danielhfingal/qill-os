FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY qill_os ./qill_os
COPY sites.example.yaml .
CMD ["python", "-m", "qill_os.core"]
