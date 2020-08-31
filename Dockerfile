FROM python:3.8.2

RUN mkdir /telegram
COPY requirements.txt /telegram
COPY telegram /telegram

RUN pip install --upgrade pip && \
    pip install -r /telegram/requirements.txt

WORKDIR /telegram
CMD ["python", "run.py"]
