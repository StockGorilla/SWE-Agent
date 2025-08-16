from mcp.server import Server
from mcp import stdio_server
import os, subprocess, requests
import asyncio

server = Server("github")

@server.call_tool()
def create_pr(branch_name: str, title: str, body: str, base="main"):
    repo = os.getenv("GH_REPO")  # e.g., owner/repo
    token = os.getenv("GH_TOKEN")
    url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {"Authorization": f"token {token}"}
    payload = {"title": title, "head": branch_name, "base": base, "body": body}
    res = requests.post(url, headers=headers, json=payload)
    res.raise_for_status()
    return {"pr_url": res.json()["html_url"]}

@server.call_tool()
def clone_repo(branch_name: str, target_dir: str):
    repo = os.getenv("GH_REPO")
    url = f"https://github.com/{repo}.git"
    subprocess.run(["git", "clone", url, target_dir])
    subprocess.run(["git", "checkout", branch_name], cwd=target_dir)
    return {"status": "cloned"}

async def main():
    async with stdio_server() as streams:
        await server.run(*streams, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
