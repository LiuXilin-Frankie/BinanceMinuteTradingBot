FROM python:3.8
#variables
ENV VIRTUAL_ENV=/myvenv

WORKDIR /crypto-signals

RUN python -m venv $VIRTUAL_ENV
# Enable venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .
RUN pip install --upgrade pip && cd ./main/ && pip install -r requirements.txt

ENTRYPOINT ["python", "./main/main.py"]
CMD ["btcusdt"]
