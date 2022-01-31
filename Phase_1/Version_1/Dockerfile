FROM python:3.9

COPY . ./code/
WORKDIR /code
ADD requirements.txt .
RUN pip install -r requirements.txt \ 
    && pip install uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]