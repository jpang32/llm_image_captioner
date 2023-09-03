FROM python:3.8

# Install Sagemaker dependencies
RUN apt-get -y update && apt-get install -y --no-install-recommends \
    libusb-1.0-0-dev \
    libudev-dev \
    build-essential \
    ca-certificates && \
    rm -fr /var/lib/apt/lists/*

# Keep python from buffering the stdout - so the logs flush quickly
ENV PYTHONUNBUFFERED=TRUE

# Don't compile bytecode
ENV PYTHONDONTWRITEBYTECODE=TRUE

ENV PATH="/opt/app:${PATH}"

ENV PYTHONPATH=.

RUN pip3 install pipenv==2022.7.4

# Install packages
WORKDIR /opt/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Add src code
COPY src ./
RUN chmod +x inference