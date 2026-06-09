import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Cpu, Activity, Wifi, AlertTriangle, Plus } from "lucide-react";
import { api, type Agent } from "@/lib/api";
import { AgentStream } from "@/components/AgentStream";

export default function Dashboard() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .listAgents()
      .then(setAgents)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const stats = {
    total: agents.length,
    online: agents.filter((a) => a.status === "online").length,
    provisioning: agents.filter((a) => a.status === "provisioning").length,
    error: agents.filter((a) => a.status === "error").length,
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="text-gray-500">Overview of your AI agent fleet</p>
        </div>
        <Link
          to="/provision"
          className="flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-500"
        >
          <Plus className="h-4 w-4" />
          New Agent
        </Link>
      </div>

      {/* Stats cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { label: "Total Agents", value: stats.total, icon: Cpu, color: "text-brand-400" },
          { label: "Online", value: stats.online, icon: Wifi, color: "text-green-400" },
          { label: "Provisioning", value: stats.provisioning, icon: Activity, color: "text-yellow-400" },
          { label: "Errors", value: stats.error, icon: AlertTriangle, color: "text-red-400" },
        ].map((stat) => {
          const Icon = stat.icon;
          return (
            <div
              key={stat.label}
              className="rounded-xl border border-gray-800 bg-gray-900 p-5"
            >
              <div className="flex items-center justify-between">
                <p className="text-sm text-gray-400">{stat.label}</p>
                <Icon className={`h-5 w-5 ${stat.color}`} />
              </div>
              <p className="mt-2 text-3xl font-bold text-white">
                {loading ? "..." : stat.value}
              </p>
            </div>
          );
        })}
      </div>

      {/* Recent agents */}
      <div>
        <h2 className="mb-4 text-lg font-semibold text-white">Recent Agents</h2>
        {loading ? (
          <p className="text-gray-500">Loading agents...</p>
        ) : agents.length === 0 ? (
          <div className="rounded-xl border border-gray-800 bg-gray-900 p-8 text-center">
            <Cpu className="mx-auto h-12 w-12 text-gray-600" />
            <h3 className="mt-4 text-lg font-medium text-gray-400">No agents yet</h3>
            <p className="mt-1 text-sm text-gray-600">
              Deploy your first agent to get started.
            </p>
            <Link
              to="/provision"
              className="mt-4 inline-flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-500"
            >
              <Plus className="h-4 w-4" />
              Deploy Agent
            </Link>
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {agents.slice(0, 6).map((agent) => (
              <Link
                key={agent.id}
                to={`/agents/${agent.id}`}
                className="rounded-xl border border-gray-800 bg-gray-900 p-4 transition-colors hover:border-brand-500/50"
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-medium text-white">{agent.name}</h3>
                  <span
                    className={`text-xs ${
                      agent.status === "online" ? "text-green-400" : "text-gray-500"
                    }`}
                  >
                    {agent.status}
                  </span>
                </div>
                <p className="mt-1 text-sm text-gray-500">{agent.host}</p>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Live event stream */}
      <AgentStream />
    </div>
  );
}
