from mcp.server import Server
from mcp import stdio_server
import subprocess
import asyncio

server = Server("sonar")

@server.call_tool()
def scan_project(repo_path: str):
    """
    Run SonarQube analysis using local Sonar Scanner CLI.
    Assumes sonar-project.properties exists in repo_path
    """
    try:
        result = subprocess.run(
            ["sonar-scanner"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        success = True
        logs = result.stdout
    except subprocess.CalledProcessError as e:
        success = False
        logs = e.stdout + "\n" + e.stderr

    return {
        "pass": success,
        "logs": logs
    }


async def main():
    async with stdio_server() as streams:
        await server.run(*streams, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
