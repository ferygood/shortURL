# base image
FROM python:3.11.3

# set working directory
WORKDIR /app

# copy requirements.txt to the container
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# Copy all the files in current path into container
COPY . .

# launch FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
