FROM python:3.8.13

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN mkdir pickles
COPY ./pickles ./pickles

COPY grpc-server.py classifier.py preprocessing.py tfidfextractor.py stopwords.txt ./
COPY classify_and_extract.proto classify_and_extract_pb2.py classify_and_extract_pb2_grpc.py ./

CMD [ "python", "./grpc-server.py" ]
