// src/components/WorkflowSummary.tsx
import React from "react";
import type { IssueResult } from "../api/workflow";
import {
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Line,
  ComposedChart,
} from "recharts";

interface Props {
  issues: IssueResult[];
}

const stages = ["planned", "coded", "reviewed", "auto_fix", "pr_created"];

const stageLabels: Record<string, string> = {
  planned: "Planner",
  coded: "Coder",
  reviewed: "Reviewer",
  auto_fix: "Auto-Fix",
  pr_created: "PR Created",
};


const WorkflowSummary: React.FC<Props> = ({ issues }) => {
  // Prepare chart data
  const data = stages.map(stage => {
    const stageIssues = issues.filter(issue => issue.fsm_history?.includes(stage));
    const passedTests = stageIssues.reduce((acc, i) => acc + (i.tests_passed || 0), 0);
    const totalTests = stageIssues.reduce((acc, i) => acc + (i.tests_total || 0), 0);
    const avgSonar =
      stageIssues.length > 0
        ? stageIssues.reduce((acc, i) => acc + (i.sonar_quality || 0), 0) / stageIssues.length
        : 0;

    return {
      stage: stageLabels[stage],
      count: stageIssues.length,
      passedTests,
      failedTests: totalTests - passedTests,
      avgSonar: Number(avgSonar.toFixed(1)),
    };
  });

  return (
    <div className="bg-white p-6 rounded-xl shadow mb-6">
      <h3 className="text-lg font-semibold mb-4">Workflow Summary</h3>
      <ResponsiveContainer width="100%" height={300}>
        <ComposedChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <XAxis dataKey="stage" />
          <YAxis yAxisId="left" allowDecimals={false} />
          <YAxis yAxisId="right" orientation="right" domain={[0, 100]} />
          <Tooltip />
          <Legend />
          {/* Stacked Bar for Tests */}
          <Bar yAxisId="left" dataKey="passedTests" stackId="a" fill="#4ade80" name="Tests Passed" />
          <Bar yAxisId="left" dataKey="failedTests" stackId="a" fill="#f87171" name="Tests Failed" />
          {/* Line for Avg Sonar */}
          <Line yAxisId="right" type="monotone" dataKey="avgSonar" stroke="#3b82f6" strokeWidth={2} name="Avg Sonar Quality" />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};

export default WorkflowSummary;
