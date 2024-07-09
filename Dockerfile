FROM python:3.11

COPY . /app


# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file\
RUN apt-get update && apt-get install -y python3-dev gcc libc-dev libffi-dev
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -  # Use the appropriate version
RUN apt-get install -y nodejs
RUN node -v
RUN npm -v

RUN pip install --upgrade pip
RUN pip install flask
RUN pip install flake8
RUN pip install pytest

WORKDIR /app/server
RUN pip install -r requirements.txt



# configure the container to run in an executed manner
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
