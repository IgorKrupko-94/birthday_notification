FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY ./birthdays .
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]