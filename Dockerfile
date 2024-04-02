FROM python:3.12.2-slim AS build-env


RUN apt-get update -y
WORKDIR /app
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use the distroless Python base image for a smaller, more secure final image
FROM gcr.io/distroless/python3-debian12

# Copy the installed packages from the build environment
COPY --from=build-env /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Set the working directory in the container
WORKDIR /app
COPY main.py .


ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages

EXPOSE 5002
ENTRYPOINT ["python", "-u", "main.py"]
