FROM python:3

ADD release_engineer_code.py /

CMD [ "python", "./release_engineer_code.py" ]
