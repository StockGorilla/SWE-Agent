import React from "react";
import type { IssueResult } from "../api/workflow";
import { BarChart, Bar, XAxis, YAxis, Tooltip, LabelList, ResponsiveContainer } from "recharts";

interface Props {
  issue: IssueResult;
}

const IssueMetrics: React.FC<Props> = ({ issue }) => {
  const testData = [
    { name: "Tests", Passed: issue.tests_passed || 0, Failed: (issue.tests_total || 0) - (issue.tests_passed || 0) },
  ];

  const sonarData = [
    { name: "Sonar Quality", Quality: issue.sonar_quality || 0 },
  ];

  return (
    <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Test Pass/Fail */}
      <div className="bg-gray-50 p-4 rounded-xl shadow">
        <h4 className="font-semibold mb-2">Test Results</h4>
        <ResponsiveContainer width="100%" height={150}>
          <BarChart data={testData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="Passed" stackId="a" fill="#4ade80">
              <LabelList dataKey="Passed" position="top" />
            </Bar>
            <Bar dataKey="Failed" stackId="a" fill="#f87171">
              <LabelList dataKey="Failed" position="top" />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Sonar Quality */}
      <div className="bg-gray-50 p-4 rounded-xl shadow">
        <h4 className="font-semibold mb-2">Sonar Quality</h4>
        <ResponsiveContainer width="100%" height={150}>
          <BarChart data={sonarData}>
            <XAxis dataKey="name" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Bar dataKey="Quality" fill="#3b82f6">
              <LabelList dataKey="Quality" position="top" />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default IssueMetrics;
