
FROM python:3.9-slim
COPY ./ /crawler/
WORKDIR /crawler/
RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip install --upgrade pip==22.0.3
RUN pip install -r requirements.txt
ENTRYPOINT [ "sh" ]