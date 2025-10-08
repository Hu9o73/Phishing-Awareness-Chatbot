FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y bash curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/ /app/

RUN pip install -r requirements.txt --root-user-action=ignore

WORKDIR /

# Cleaning .sh file if the file comes from a windows computer
RUN sed -i 's/\r$//' ./app/run_unit_tests.sh

CMD ["bash", "./app/run_unit_tests.sh"]
