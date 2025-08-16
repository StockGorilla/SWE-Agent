# backend/orchestrator/mcp_client.py

from mcp.server import Server

# Create MCP servers for each agent type
jira_client = Server("jira")
github_client = Server("github")
maven_client = Server("maven")
filesystem_client = Server("filesystem")
sonar_client = Server("sonar")
