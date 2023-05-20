FROM python:3.9

EXPOSE 5000

WORKDIR keyrace

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-m", "flask", "--app", "app", "run"]