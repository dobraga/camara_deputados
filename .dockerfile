FROM python:3.8.0-buster

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /
COPY /app /app/.
COPY teste.py .

CMD ["python", "teste.py"]