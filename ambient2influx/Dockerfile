FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY ambient2influx.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP ambient2influx.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]