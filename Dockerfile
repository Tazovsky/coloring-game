FROM python:3.9.4

WORKDIR /game

COPY requirements.txt main.py .
COPY funs/ funs/

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]