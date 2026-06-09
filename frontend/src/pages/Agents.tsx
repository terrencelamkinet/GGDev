import { useEffect, useState } from "react";
import { Cpu } from "lucide-react";
import { api, type Agent } from "@/lib/api";
import { AgentCard } from "@/components/AgentCard";

export default function Agents() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .listAgents()
      .then(setAgents)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Cpu className="h-8 w-8 animate-pulse text-brand-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Agents</h1>
        <p className="text-gray-500">
          {agents.length} agent{agents.length !== 1 ? "s" : ""} registered
        </p>
      </div>

      {agents.length === 0 ? (
        <div className="rounded-xl border border-gray-800 bg-gray-900 p-12 text-center">
          <Cpu className="mx-auto h-16 w-16 text-gray-700" />
          <h2 className="mt-4 text-xl font-semibold text-gray-400">No Agents</h2>
          <p className="mt-2 text-sm text-gray-600">
            Deploy your first agent via the Provision page.
          </p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {agents.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>
      )}
    </div>
  );
}
