FROM python:3.9

WORKDIR /code
COPY * /code/
RUN pip install -r requirements.txt
EXPOSE 90
CMD [ "python", "boberto.py" ]