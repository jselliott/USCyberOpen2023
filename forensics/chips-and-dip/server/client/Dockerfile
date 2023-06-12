FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl

COPY flag.txt /flag.txt

RUN mkdir /app

WORKDIR /app

COPY malware.sh .
RUN chmod +x malware.sh

CMD ["./malware.sh"]