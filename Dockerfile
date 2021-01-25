FROM python:3.7

RUN pip install pipenv

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src/ .

COPY ./scripts/punkt.py .
RUN pwd && python punkt.py

COPY ./scripts/corpus.py .
RUN pwd && python corpus.py

ENV FLASK_APP main.py

CMD [ "gunicorn", "-w", "4", "-b", ":443", "--certfile", "/certs/fullchain.pem", "--keyfile", "/certs/privkey.pem", "main:app" ]


