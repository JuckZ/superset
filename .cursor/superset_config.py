# superset_config.py
from superset.mcp_service.mcp_config import DEFAULT_MCP_CONFIG

# Basic configuration
MCP_DEV_USERNAME = "admin"  # User for development/testing
MCP_SERVICE_HOST = "localhost"
MCP_SERVICE_PORT = 5008

# Optional: JWT authentication for production
# MCP_AUTH_ENABLED = True
# MCP_JWT_PUBLIC_KEY = "your_public_key_here"
# MCP_JWT_ALGORITHM = "RS256"

# Optional: Screenshot configuration
WEBDRIVER_BASEURL = "http://localhost:8088/"
WEBDRIVER_TYPE = "chrome"