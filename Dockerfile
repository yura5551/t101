FROM python:3.7-slim-buster
ADD main.py /
CMD [ "python3", "main.py" ]