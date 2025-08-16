from orchestrator.agents.reviewer import reviewer
from orchestrator.gemini_client import gemini_model
from orchestrator.mcp_client import filesystem_client, maven_client
import os

MAX_FIX_ROUNDS = 3

def auto_fix(coded_task):
    fsm = coded_task.get("fsm")
    round_num = 1
    while round_num <= MAX_FIX_ROUNDS:
        result = reviewer(coded_task)
        if result["workflow_status"] == "success":
            return result

        # Generate fix using Gemini
        fix_prompt = f"""The following code failed tests or Sonar scan. Suggest fixes.
        Plan:\n{coded_task['plan']}
        Test logs:\n{result['test_result']['stdout']}
        Sonar logs:\n{result['sonar_result'].get('logs')}
        Provide only corrected code."""
        fixed_code = gemini_model.generate_text(fix_prompt)
        filesystem_client.write_file(
            path=os.path.join(coded_task["target_dir"], "Example.java"),
            content=fixed_code
        )

        coded_task["test_result"] = maven_client.run_tests(repo_path=coded_task["target_dir"])
        round_num += 1

        if fsm:
            fsm.transition("auto_fix")

    return reviewer(coded_task)
