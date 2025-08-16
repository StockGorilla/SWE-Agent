from orchestrator.gemini_client import gemini_model

def planner(issue, fsm=None):
    issue_id = issue["id"]
    issue_summary = issue["fields"]["summary"]

    plan_prompt = f"Create a coding plan for Jira issue: {issue_summary}"
    plan = gemini_model.generate_text(plan_prompt)

    if fsm:
        fsm.transition("planned")

    return {"issue_id": issue_id, "plan": plan, "issue_summary": issue_summary, "fsm": fsm}
