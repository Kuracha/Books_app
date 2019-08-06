FROM python:3.7-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY . .

RUN pip install --upgrade pip
RUN pip install pipenv
RUN chmod +x ./entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["sh","./entrypoint.sh" ]