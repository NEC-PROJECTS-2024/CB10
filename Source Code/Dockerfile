FROM python:3.10
WORKDIR /app
COPY . /app
RUN apt-get update && \
    pip install -r requirements.txt && \
    chmod -R 777 /app && \
    chmod -R 777 /app


EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["bird.py", "runserver", "0.0.0.0:5000"]