FROM python:3.9-alpine
RUN mkdir /app
WORKDIR /app
RUN touch /app/database.sqlite3
ADD requirements.txt /app
ADD main.py /app
ADD .env /app/.env
ADD ./templates /app/templates/
RUN pip3 install -r requirements.txt
CMD ["python", "main.py"]
