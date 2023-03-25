FROM tiangolo/uvicorn-gunicorn-fastapi

COPY ./app /app

COPY ./requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY . .

CMD ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "8000"] 
