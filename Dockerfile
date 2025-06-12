# Use a lightweight Debian image
FROM debian:bookworm-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y baresip python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Set working directory
WORKDIR /app

# Copy application files
COPY app/ /app/app/
COPY config/ /app/config/
COPY recordings/ /app/recordings/
COPY templates/ /app/templates/
COPY static/ /app/static/
COPY run.sh /app/
COPY requirements.txt /app/

# Make run.sh executable
RUN chmod +x /app/run.sh

# Expose Web GUI port
EXPOSE 8080

# Optionally expose SIP UDP port if needed for external SIP registration
# EXPOSE 5060/udp

# Set default command
CMD ["bash", "/app/run.sh"]
