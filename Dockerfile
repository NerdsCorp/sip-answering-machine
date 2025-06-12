# Use a modern Python 3 base image
FROM python:3.9-slim

# Install system dependencies for building PJSIP and running the app
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    python3-dev \
    python3-pip \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and build PJSIP with Python 3 bindings
RUN wget https://github.com/pjsip/pjproject/archive/refs/tags/2.15.1.tar.gz \
    && tar xzf 2.15.1.tar.gz \
    && cd pjproject-2.15.1 \
    && ./configure --enable-shared --with-python \
    && make \
    && make install \
    && ldconfig \
    && cd pjsip-apps/src/python \
    && python3 setup.py install

WORKDIR /app

# Copy your application code into the image
COPY . .

# Install Python dependencies
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "app/main.py"]

EXPOSE 8080

CMD ["python", "main.py"]
