FROM python:3.11

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

#Expose port 5000, on which the Flask application runs
EXPOSE 5000

CMD ["python", "website/main.py"]
