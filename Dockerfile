FROM tiangolo/uwsgi-nginx:python3.7

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./app.py"]
