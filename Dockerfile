## Chainguard Python Dockerfile 
## Doc link: https://images.chainguard.dev/directory/image/python/overview
FROM cgr.dev/chainguard/python:latest-dev AS build-env

USER root
RUN apk update

USER nonroot
WORKDIR /app
RUN python -m venv venv
ENV PATH="/app/venv/bin":$PATH
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM cgr.dev/chainguard/python:latest

WORKDIR /app

COPY main.py .
COPY --from=build-env /app/venv /app/venv

ENV PATH="/app/venv/bin:$PATH"

EXPOSE 5002
ENTRYPOINT ["python", "-u", "main.py"]
