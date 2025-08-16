# MCP Servers Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Maven for Maven MCP server
RUN apt-get update && apt-get install -y maven && rm -rf /var/lib/apt/lists/*

# Copy requirements from backend (MCP servers use same dependencies)
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy MCP server code
COPY mcp_servers/ ./mcp_servers/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Default command (will be overridden by docker-compose)
CMD ["python", "mcp_servers/jira_mcp_server.py"]
