from mcp.server import Server
from mcp import stdio_server
import subprocess
import asyncio

server = Server("maven")

@server.call_tool()
def run_tests(repo_path: str):
    result = subprocess.run(
        ["mvn", "-B", "test"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr
    }

@server.call_tool()
def build_project(repo_path: str):
    result = subprocess.run(
        ["mvn", "-B", "clean", "install"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr
    }

async def main():
    async with stdio_server() as streams:
        await server.run(*streams, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
