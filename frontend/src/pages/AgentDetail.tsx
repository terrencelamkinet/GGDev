import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft, Cpu, Globe, Clock, Key, Wifi, WifiOff, Loader2, AlertTriangle } from "lucide-react";
import { api, type Agent } from "@/lib/api";
import { AgentStream } from "@/components/AgentStream";

const statusDisplay: Record<string, { icon: typeof Wifi; color: string; label: string }> = {
  online: { icon: Wifi, color: "text-green-400", label: "Online" },
  offline: { icon: WifiOff, color: "text-gray-500", label: "Offline" },
  provisioning: { icon: Loader2, color: "text-yellow-400", label: "Provisioning" },
  error: { icon: AlertTriangle, color: "text-red-400", label: "Error" },
};

export default function AgentDetail() {
  const { id } = useParams<{ id: string }>();
  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    api
      .getAgent(id)
      .then(setAgent)
      .catch(() => setAgent(null))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="h-8 w-8 animate-spin text-brand-400" />
      </div>
    );
  }

  if (!agent) {
    return (
      <div className="space-y-4">
        <Link to="/agents" className="inline-flex items-center gap-1 text-sm text-brand-400 hover:underline">
          <ArrowLeft className="h-4 w-4" />
          Back to agents
        </Link>
        <div className="rounded-xl border border-red-800 bg-red-900/20 p-6">
          <p className="text-red-400">Agent not found.</p>
        </div>
      </div>
    );
  }

  const status = statusDisplay[agent.status] ?? statusDisplay.offline;
  const StatusIcon = status.icon;

  return (
    <div className="space-y-6">
      <Link to="/agents" className="inline-flex items-center gap-1 text-sm text-brand-400 hover:underline">
        <ArrowLeft className="h-4 w-4" />
        Back to agents
      </Link>

      {/* Agent header */}
      <div className="rounded-xl border border-gray-800 bg-gray-900 p-6">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-gray-800">
              <Cpu className="h-7 w-7 text-brand-400" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">{agent.name}</h1>
              <div className="mt-1 flex items-center gap-2">
                <StatusIcon className={`h-4 w-4 ${status.color}`} />
                <span className={`text-sm ${status.color}`}>{status.label}</span>
                <span className="text-gray-600">·</span>
                <span className="text-sm text-gray-500">{agent.role}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 grid gap-4 sm:grid-cols-3">
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <Globe className="h-4 w-4" />
            <span>{agent.host}:{agent.port}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <Clock className="h-4 w-4" />
            <span>
              {agent.last_heartbeat
                ? new Date(agent.last_heartbeat).toLocaleString()
                : "No heartbeat yet"}
            </span>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <Key className="h-4 w-4" />
            <span className="font-mono">
              {agent.api_key ? `${agent.api_key.slice(0, 12)}...` : "No API key"}
            </span>
          </div>
        </div>
      </div>

      {/* Live event stream */}
      <AgentStream />
    </div>
  );
}
