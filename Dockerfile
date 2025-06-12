# Use a lightweight Debian image
FROM debian:bookworm-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (including for venv)
RUN apt-get update && \
    apt-get install -y baresip python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Upgrade pip in the venv
RUN /opt/venv/bin/pip install --upgrade pip

# Set the PATH so venv is default
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy requirements first for Docker cache efficiency
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies in the venv
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy application files
COPY . .


# Create recordings directory
RUN mkdir -p /app/recordings/

# Make run.sh executable
RUN chmod +x /app/run.sh

# Expose Web GUI port
EXPOSE 8080

# Optionally expose SIP UDP port if needed for external SIP registration
EXPOSE 5060/udp

# Set default command
CMD ["bash", "/app/run.sh"]
