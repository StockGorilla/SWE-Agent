from orchestrator.mcp_client import sonar_client, github_client, jira_client

def reviewer(coded_task):
    fsm = coded_task.get("fsm")
    if fsm:
        fsm.transition("reviewed")

    issue_id = coded_task["issue_id"]
    branch_name = coded_task["branch_name"]
    target_dir = coded_task["target_dir"]
    plan = coded_task["plan"]
    test_result = coded_task["test_result"]

    sonar_result = sonar_client.scan_project(repo_path=target_dir)

    workflow_status = "failed"
    pr_url = None
    logs = None

    if test_result["success"] and sonar_result["pass"]:
        pr_title = f"Auto PR for Jira {issue_id}"
        pr_body = f"Plan:\n{plan}"
        pr_info = github_client.create_pr(branch_name=branch_name, title=pr_title, body=pr_body)
        jira_client.update_issue(issue_id=issue_id, comment=f"PR created: {pr_info['pr_url']}")
        workflow_status = "success"
        pr_url = pr_info["pr_url"]
        if fsm:
            fsm.transition("pr_created")
    else:
        logs = {
            "test_stdout": test_result["stdout"],
            "test_stderr": test_result["stderr"],
            "sonar_logs": sonar_result.get("logs")
        }
        if fsm:
            fsm.transition("auto_fix")

    return {"issue_id": issue_id, "workflow_status": workflow_status, "pr_url": pr_url,
            "logs": logs, "target_dir": target_dir, "test_result": test_result,
            "sonar_result": sonar_result, "plan": plan, "fsm": fsm}
