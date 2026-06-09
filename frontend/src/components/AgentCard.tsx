import type { Agent } from "@/lib/api";
import { Link } from "react-router-dom";
import { Cpu, Globe, Clock, Wifi, WifiOff, AlertTriangle, Loader2 } from "lucide-react";

const statusConfig: Record<string, { icon: typeof Wifi; color: string; label: string }> = {
  online: { icon: Wifi, color: "text-green-400", label: "Online" },
  offline: { icon: WifiOff, color: "text-gray-500", label: "Offline" },
  provisioning: { icon: Loader2, color: "text-yellow-400", label: "Provisioning" },
  error: { icon: AlertTriangle, color: "text-red-400", label: "Error" },
};

interface AgentCardProps {
  agent: Agent;
}

export function AgentCard({ agent }: AgentCardProps) {
  const status = statusConfig[agent.status] ?? statusConfig.offline;
  const StatusIcon = status.icon;

  return (
    <Link
      to={`/agents/${agent.id}`}
      className="group block rounded-xl border border-gray-800 bg-gray-900 p-5 transition-all hover:border-brand-500/50 hover:shadow-lg hover:shadow-brand-500/5"
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gray-800">
            <Cpu className="h-5 w-5 text-brand-400" />
          </div>
          <div>
            <h3 className="font-semibold text-white group-hover:text-brand-400">
              {agent.name}
            </h3>
            <p className="text-sm text-gray-500">{agent.role}</p>
          </div>
        </div>

        <div className={`flex items-center gap-1.5 rounded-full bg-gray-800 px-3 py-1 text-xs ${status.color}`}>
          <StatusIcon className={`h-3.5 w-3.5 ${agent.status === "provisioning" ? "animate-spin" : ""}`} />
          {status.label}
        </div>
      </div>

      <div className="mt-4 flex items-center gap-4 text-sm text-gray-500">
        <span className="flex items-center gap-1">
          <Globe className="h-3.5 w-3.5" />
          {agent.host}:{agent.port}
        </span>
        <span className="flex items-center gap-1">
          <Clock className="h-3.5 w-3.5" />
          {agent.last_heartbeat
            ? new Date(agent.last_heartbeat).toLocaleString()
            : "Never"}
        </span>
      </div>
    </Link>
  );
}
