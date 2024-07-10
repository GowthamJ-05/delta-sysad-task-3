FROM python:latest
COPY . /app
WORKDIR /app/server
RUN pip install -r requirements.txt
ENV PORT 5000
EXPOSE $PORT

CMD ["python", "app-server.py"]
