FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U flask-cors
RUN pip install --upgrade Werkzeug
COPY src/* .

CMD ["python", "app.py"]