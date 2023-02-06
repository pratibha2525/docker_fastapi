FROM python:3.10-slim-buster
RUN apt-get update && apt-get  install -y wkhtmltopdf
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY . /app/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "src.main:app"]

