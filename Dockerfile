FROM getflow/python-poetry:stable-python3.9 as base

WORKDIR /app/

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
&& poetry install --without dev

COPY backend .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]