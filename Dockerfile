FROM python:3.9-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY main.py requirements.txt /srv/
WORKDIR /srv/
RUN uv pip install -r requirements.txt --system
