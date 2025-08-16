from mcp.server import Server
from mcp import stdio_server
import os, requests
import asyncio

server = Server("jira")

@server.call_tool()
def list_issues(assignee: str):
    url = f"{os.getenv('JIRA_URL')}/rest/api/3/search"
    headers = {"Authorization": f"Bearer {os.getenv('JIRA_TOKEN')}"}
    jql = f"assignee={assignee} AND status='To Do'"
    res = requests.get(url, headers=headers, params={"jql": jql})
    res.raise_for_status()
    return res.json().get("issues", [])

@server.call_tool()
def update_issue(issue_id: str, comment: str):
    url = f"{os.getenv('JIRA_URL')}/rest/api/3/issue/{issue_id}/comment"
    headers = {"Authorization": f"Bearer {os.getenv('JIRA_TOKEN')}"}
    res = requests.post(url, headers=headers, json={"body": comment})
    return {"status": res.status_code}

async def main():
    async with stdio_server() as streams:
        await server.run(*streams, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
