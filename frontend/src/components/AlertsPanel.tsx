// src/components/AlertsPanel.tsx
import React from "react";
import type { IssueResult } from "../api/workflow";

interface Props {
  issues: IssueResult[];
}

const AlertsPanel: React.FC<Props> = ({ issues }) => {
  const prReady = issues.filter(issue => issue.pr_url);
  const testFailures = issues.filter(
    issue => (issue.tests_passed || 0) < (issue.tests_total || 0)
  );
  const lowSonar = issues.filter(issue => (issue.sonar_quality || 100) < 70);

  return (
    <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
      {/* PR Ready */}
      <div className="bg-green-50 p-4 rounded-xl shadow">
        <h3 className="font-semibold mb-2">PR Ready ({prReady.length})</h3>
        <ul className="text-sm text-gray-700">
          {prReady.map(issue => (
            <li key={issue.issue_id}>
              <a href={issue.pr_url} target="_blank" className="text-blue-600 underline">
                Issue {issue.issue_id}
              </a>
            </li>
          ))}
        </ul>
      </div>

      {/* Test Failures */}
      <div className="bg-red-50 p-4 rounded-xl shadow">
        <h3 className="font-semibold mb-2">Test Failures ({testFailures.length})</h3>
        <ul className="text-sm text-gray-700">
          {testFailures.map(issue => (
            <li key={issue.issue_id}>
              Issue {issue.issue_id}: {issue.tests_passed}/{issue.tests_total} tests passed
            </li>
          ))}
        </ul>
      </div>

      {/* Low Sonar */}
      <div className="bg-yellow-50 p-4 rounded-xl shadow">
        <h3 className="font-semibold mb-2">Low Sonar ({lowSonar.length})</h3>
        <ul className="text-sm text-gray-700">
          {lowSonar.map(issue => (
            <li key={issue.issue_id}>
              Issue {issue.issue_id}: {issue.sonar_quality}% quality
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AlertsPanel;
