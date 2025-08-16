import React, { useState } from "react";
import { useWorkflow } from "../hooks/useWorkflow";
import IssueCard from "./IssueCard";
import WorkflowSummary from "./WorkflowSummary";
import AlertsPanel from "./AlertsPanel";

type Filter = "all" | "prReady" | "failedTests" | "lowSonar";

const Dashboard: React.FC = () => {
  const { data, isLoading, error } = useWorkflow();
  const [filter, setFilter] = useState<Filter>("all");

  if (isLoading) return <p className="text-center mt-10">Loading workflow...</p>;
  if (error) return <p className="text-center mt-10 text-red-500">Error loading workflow</p>;

  // Apply filter
  let filteredIssues = data || [];
  if (filter === "prReady") filteredIssues = filteredIssues.filter(issue => issue.pr_url);
  if (filter === "failedTests") filteredIssues = filteredIssues.filter(issue => (issue.tests_passed || 0) < (issue.tests_total || 0));
  if (filter === "lowSonar") filteredIssues = filteredIssues.filter(issue => (issue.sonar_quality || 100) < 70);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">AI Multi-Agent Workflow Dashboard</h1>

      {/* Filter Buttons */}
      <div className="flex flex-wrap gap-3 mb-6">
        <button
          className={`px-4 py-2 rounded-full font-semibold ${filter === "all" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-700"}`}
          onClick={() => setFilter("all")}
        >
          All
        </button>
        <button
          className={`px-4 py-2 rounded-full font-semibold ${filter === "prReady" ? "bg-green-500 text-white" : "bg-gray-200 text-gray-700"}`}
          onClick={() => setFilter("prReady")}
        >
          PR Ready
        </button>
        <button
          className={`px-4 py-2 rounded-full font-semibold ${filter === "failedTests" ? "bg-red-500 text-white" : "bg-gray-200 text-gray-700"}`}
          onClick={() => setFilter("failedTests")}
        >
          Test Failures
        </button>
        <button
          className={`px-4 py-2 rounded-full font-semibold ${filter === "lowSonar" ? "bg-yellow-500 text-white" : "bg-gray-200 text-gray-700"}`}
          onClick={() => setFilter("lowSonar")}
        >
          Low Sonar
        </button>
      </div>

      {/* Alerts Panel */}
      {data && <AlertsPanel issues={filteredIssues} />}

      {/* Workflow Summary */}
      {data && <WorkflowSummary issues={filteredIssues} />}

      {/* Individual Issue Cards */}
      {filteredIssues?.map(issue => (
        <IssueCard key={issue.issue_id} issue={issue} />
      ))}
    </div>
  );
};

export default Dashboard;
