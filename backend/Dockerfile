FROM python:3.8 AS builder

RUN python -m venv /venv;

WORKDIR /code

COPY ./requirements.txt  .

RUN /venv/bin/pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.8-slim

WORKDIR /code

COPY --from=builder /venv/ /venv/ 

ENV PATH=/venv/bin:$PATH

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
