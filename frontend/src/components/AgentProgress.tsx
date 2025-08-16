// src/components/AgentProgress.tsx
import React from "react";
import { Tooltip } from "react-tooltip";
import type { PlacesType } from "react-tooltip";

interface Props {
  history?: string[];
  logs?: Record<string, string>;
}

const AgentProgress: React.FC<Props> = ({ history = [], logs = {} }) => {
  const stages = ["planned", "coded", "reviewed", "auto_fix", "pr_created"];
  const tooltipPlace: PlacesType = "top";

  return (
    <div className="mt-4 flex items-center space-x-2">
      {stages.map(stage => {
        const completed = history.includes(stage);
        return (
          <div key={stage} className="relative flex flex-col items-center">
            <div
              data-tooltip-id={`tooltip-${stage}`}
              className={`w-5 h-5 rounded-full ${completed ? "bg-green-500" : "bg-gray-300"}`}
            />
            <span className="text-xs mt-1">{stage}</span>

            {/* Tooltip for logs */}
            {completed && logs[stage] && (
              <Tooltip
                id={`tooltip-${stage}`}
                place={tooltipPlace}
              >
                {logs[stage]}
              </Tooltip>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default AgentProgress;
