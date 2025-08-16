from mcp.server import Server
from mcp import stdio_server
import os
import subprocess
import asyncio

server = Server("filesystem")

@server.call_tool()
def read_file(path: str):
    with open(path, "r") as f:
        return f.read()

@server.call_tool()
def write_file(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)
    return {"status": "ok"}

@server.call_tool()
def apply_patch(patch_content: str, repo_path: str):
    patch_file = os.path.join(repo_path, "tmp_patch.diff")
    with open(patch_file, "w") as f:
        f.write(patch_content)
    subprocess.run(["git", "apply", patch_file], cwd=repo_path)
    os.remove(patch_file)
    return {"status": "applied"}

async def main():
    async with stdio_server() as streams:
        await server.run(*streams, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
