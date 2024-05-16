FROM python:3.10.12

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD fastapi run --port 8000

##### docker run -dit -p 8000:8000 facecare