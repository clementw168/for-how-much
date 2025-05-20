ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim-buster

RUN apt-get update && \
    apt-get -y install git gcc g++ && \
    apt-get clean

WORKDIR /src

COPY ./pyproject.toml ./
COPY ./uv.lock ./
RUN pip3 install uv && \
    uv venv && \
    uv pip install .


COPY . .

CMD ["uv", "run", "uvicorn", "main:app", "--reload"]
