// src/hooks/useWorkflow.ts
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import type { IssueResult } from "../api/workflow";

const fetchWorkflow = async (): Promise<IssueResult[]> => {
  const response = await axios.get("http://localhost:5050/api/issues"); // adjust your Flask endpoint
  return response.data;
};

export const useWorkflow = () => {
  return useQuery<IssueResult[], Error>({
    queryKey: ["workflow"],
    queryFn: fetchWorkflow,
    refetchInterval: 3000, // poll every 3 seconds
    refetchOnWindowFocus: true,
  });
};
