FROM python:3.8 AS builder

COPY ./requirements.txt .

RUN pip install --user -r requirements.txt 

FROM python:3.8-slim

WORKDIR /code

COPY --from=builder /root/.local /root/.local

COPY ./app.py .

ENV PATH=/root/.local:$PATH

CMD ["python", "./app.py", "--host=0.0.0.0"]
