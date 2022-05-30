FROM python:3.7

RUN apt update -y  &&  apt upgrade -y && apt-get update 

WORKDIR /app

COPY . /app/

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

# CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
CMD ["gunicorn", "wsgi:application", "--bind", ":8000", "--workers", "10"]