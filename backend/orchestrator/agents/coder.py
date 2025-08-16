import os, uuid
from orchestrator.mcp_client import github_client, filesystem_client, maven_client

def coder(planned_task):
    issue_id = planned_task["issue_id"]
    plan = planned_task["plan"]
    fsm = planned_task.get("fsm")

    branch_name = f"feature/{issue_id}-{uuid.uuid4().hex[:6]}"
    target_dir = f"/tmp/{branch_name}"

    github_client.clone_repo(branch_name=branch_name, target_dir=target_dir)

    filesystem_client.write_file(
        path=os.path.join(target_dir, "Example.java"),
        content=f"// Generated code for issue {issue_id}\n// Plan:\n{plan}"
    )

    test_result = maven_client.run_tests(repo_path=target_dir)

    if fsm:
        fsm.transition("coded")

    return {"issue_id": issue_id, "branch_name": branch_name, "target_dir": target_dir,
            "test_result": test_result, "plan": plan, "fsm": fsm}
