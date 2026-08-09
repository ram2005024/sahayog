FROM python:3.11-slim
WORKDIR /code
COPY pyproject.toml .
COPY uv.lock .
RUN pip install uv
RUN uv sync
COPY . .
CMD [ "uv","run","uvicorn","app.main:app","--host","0.0.0.0","--port","8000" ]
