from concurrent.futures import ThreadPoolExecutor, as_completed
from orchestrator.agents import planner, coder, auto_fix
from orchestrator.mcp_client import jira_client
from orchestrator.fsm import IssueFSM

MAX_WORKERS = 3

def run_multi_issue_workflow(assignee="AI-Agent"):
    issues = jira_client.list_issues(assignee=assignee)
    if not issues:
        return []

    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Step 1: Planning
        planned_tasks = []
        futures = []
        for issue in issues:
            fsm = IssueFSM(issue_id=issue["id"])
            futures.append(executor.submit(planner, issue, fsm))
        planned_tasks = [f.result() for f in as_completed(futures)]

        # Step 2: Coding
        coded_tasks = [f.result() for f in as_completed(
            [executor.submit(coder, task) for task in planned_tasks]
        )]

        # Step 3: Reviewing + Auto-Fix
        future_to_task = {executor.submit(auto_fix, task): task for task in coded_tasks}
        results = [f.result() for f in as_completed(future_to_task)]

    # Include FSM history in final results
    for res in results:
        fsm = res.get("fsm")
        if fsm:
            res["fsm_history"] = fsm.get_history()
            res["fsm_state"] = fsm.get_state()

    return results
