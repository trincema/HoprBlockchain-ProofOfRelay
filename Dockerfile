# Container image that runs your code
FROM python:3

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]