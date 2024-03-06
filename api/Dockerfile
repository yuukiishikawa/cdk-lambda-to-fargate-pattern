# set up the container.
FROM python:3.10-slim

# set the working dir.
WORKDIR /app
ADD . /app

# install libraries.
RUN python3 -m pip install -r requirements.txt

# command to run the app using uvicorn.
CMD ["python3", "-m", "app"]
