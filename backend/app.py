# backend/app.py

from flask import Flask, jsonify
from orchestrator.mcp_client import jira_client, github_client, maven_client, filesystem_client, sonar_client

app = Flask(__name__)

# Example endpoint to get all issues
@app.route("/api/issues")
def get_issues():
    # Replace with actual MCP calls to fetch issue status
    issues = [
        {
            "issue_id": "ISSUE-1",
            "fsm_state": "planned",
            "plan": "Implement login feature",
            "fsm_logs": {"planned": "Planning completed"},
            "auto_fix_rounds": 0,
            "pr_url": None,
            "tests_passed": 0,
            "tests_total": 0,
            "sonar_quality": 0
        },
        {
            "issue_id": "ISSUE-2",
            "fsm_state": "coded",
            "plan": "Create payment API",
            "fsm_logs": {"planned": "Planning done", "coded": "Code completed"},
            "auto_fix_rounds": 1,
            "pr_url": "http://github.com/example/pr/2",
            "tests_passed": 5,
            "tests_total": 5,
            "sonar_quality": 95
        }
    ]
    return jsonify(issues)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
