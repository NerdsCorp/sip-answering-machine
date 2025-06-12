# Use a recent Python image
FROM python:2.7-slim

# Install system dependencies
RUN apt-get update && apt-get install -y python3 python3-pip wget \
    && wget https://github.com/pjsip/pjproject/archive/refs/tags/2.15.1.tar.gz \
    && tar xzf 2.15.1.tar.gz \
    && cd pjproject-2.15.1 \
    && ./configure --enable-shared --with-python \
    && make \
    && make install \
    && ldconfig \
    && cd pjsip-apps/src/python \
    && 2to3 -w setup.py \
    && sed -i 's/\t/    /g' setup.py \
    && sed -i '/if len(tokens)>1:/i \        tokens = line.split()' setup.py \
    && python3 setup.py install
    
WORKDIR /usr/src

# Download and build PJSIP with Python bindings (pjsua2)
RUN wget https://github.com/pjsip/pjproject/archive/refs/tags/2.15.1.tar.gz \
    && tar xzf 2.15.1.tar.gz \
    && cd pjproject-2.15.1 \
    && ./configure --enable-shared --with-python \
    && make \
    && make install \
    && ldconfig \
    && cd pjsip-apps/src/python \
    && sed -i 's/\t/    /g' setup.py \
    && python3 setup.py install

WORKDIR /app

# Copy your application code into the image
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]
