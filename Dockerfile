FROM python:3.9
EXPOSE 5000
WORKDIR /code
COPY . /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "80", "--reload"]
