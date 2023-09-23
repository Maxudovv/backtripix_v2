FROM python:3.9.18


WORKDIR /app/
RUN cd /app/

COPY Pipfile.lock Pipfile /app/

RUN apt update && apt install -y pipenv
RUN pipenv --python python3 && pipenv install

COPY backend .

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]