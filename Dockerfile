FROM python:3.7

# copy required files
COPY . /app
WORKDIR /app

#Install the dependencies
RUN pip install --upgrade -r requirements-prd.txt
RUN pip install "pymongo[srv]"

EXPOSE 5001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]