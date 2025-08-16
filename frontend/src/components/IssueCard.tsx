// src/components/IssueCard.tsx
import React from "react";
import type { IssueResult } from "../api/workflow";
import AgentProgress from "./AgentProgress";
import PRLink from "./PRLink";
import IssueMetrics from "./IssueMetrics";

interface Props {
  issue: IssueResult;
}

const IssueCard: React.FC<Props> = ({ issue }) => {
  // Determine alert statuses
  const hasPR = !!issue.pr_url;
  const failedTests = (issue.tests_passed || 0) < (issue.tests_total || 0);
  const lowSonar = (issue.sonar_quality || 100) < 70;

  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 mb-6 border-l-4 border-blue-500">
      {/* Issue Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Issue {issue.issue_id}</h3>
        <div className="flex space-x-2">
          {hasPR && <span className="px-2 py-1 text-xs font-bold bg-green-200 text-green-800 rounded-full">PR Ready</span>}
          {failedTests && <span className="px-2 py-1 text-xs font-bold bg-red-200 text-red-800 rounded-full">Test Fail</span>}
          {lowSonar && <span className="px-2 py-1 text-xs font-bold bg-yellow-200 text-yellow-800 rounded-full">Low Sonar</span>}
        </div>
      </div>

      <p className="mt-2 text-gray-600">
        Current State: <span className="font-bold">{issue.fsm_state}</span>
      </p>

      {/* Completion Percentage */}
      {issue.fsm_history && (
        <p className="mt-2 text-sm text-gray-600">
          Completion: <span className="font-bold">{Math.floor((issue.fsm_history.length / 5) * 100)}%</span>
        </p>
      )}

      {/* Plan */}
      <div className="mt-4">
        <h4 className="font-medium text-gray-700">Plan:</h4>
        <p className="bg-gray-100 p-3 rounded-md whitespace-pre-wrap">{issue.plan}</p>
      </div>

      {/* Animated Agent Progress with tooltips */}
      <AgentProgress history={issue.fsm_history} logs={issue.fsm_logs} />

      {/* Auto-Fix Rounds */}
      {issue.auto_fix_rounds !== undefined && (
        <p className="mt-2 text-sm text-gray-600">
          Auto-Fix Rounds: <span className="font-bold">{issue.auto_fix_rounds}</span>
        </p>
      )}

      {/* Metrics Charts: Tests & Sonar */}
      <IssueMetrics issue={issue} />

      {/* PR Link */}
      {hasPR && <PRLink url={issue.pr_url || ""} />}
    </div>
  );
};

export default IssueCard;
