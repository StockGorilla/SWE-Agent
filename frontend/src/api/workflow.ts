import axios from "axios";

export interface IssueResult {
  issue_id: string;
  fsm_state: string;
  fsm_history: string[];
  fsm_logs?: Record<string, string>;
  plan: string;
  workflow_status: string;
  pr_url?: string;
  logs?: any;

  // New fields for metrics
  auto_fix_rounds?: number;
  tests_passed?: number;
  tests_total?: number;
  sonar_quality?: number; // 0-100
}

export const fetchWorkflowResults = async (): Promise<IssueResult[]> => {
  const res = await axios.post("http://localhost:5050/run_tasks", {
    assignee: "AI-Agent"
  });
  return res.data.results;
};
