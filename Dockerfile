# Use a recent Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    wget \
    libasound2-dev \
    libsndfile1 \
    git \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src

# Download and build PJSIP with Python bindings (pjsua2)
RUN wget https://github.com/pjsip/pjproject/archive/refs/tags/2.13.tar.gz \
    && tar xzf 2.13.tar.gz \
    && cd pjproject-2.13 \
    && ./configure --enable-shared --with-python \
    && make \
    && make install \
    && ldconfig \
    # Fix tabs to spaces in setup.py
    && sed -i 's/\t/    /g' pjsip-apps/src/python/setup.py \
    # Fix Python 2 print statements to Python 3 print() function
    && sed -i "s/print '\\(.*\\)'/print('\\1')/g" pjsip-apps/src/python/setup.py \
    # Fix any remaining print statements (handles double quotes)
    && sed -i 's/print "\(.*\)"/print("\1")/g' pjsip-apps/src/python/setup.py \
    && cd pjsip-apps/src/python \
    && python3 setup.py install

WORKDIR /app

# Copy your application code into the image
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]
