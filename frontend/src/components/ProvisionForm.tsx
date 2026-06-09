import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Terminal, Server, User, Lock, Loader2 } from "lucide-react";
import { api, type ProvisionResponse } from "@/lib/api";

type StepStatus = "idle" | "running" | "success" | "error";

interface Step {
  label: string;
  status: StepStatus;
  message?: string;
}

const initialSteps: Step[] = [
  { label: "SSH Connection", status: "idle" },
  { label: "OS Detection", status: "idle" },
  { label: "Docker Install", status: "idle" },
  { label: "Agent Deploy", status: "idle" },
  { label: "Health Check", status: "idle" },
  { label: "Registration", status: "idle" },
];

export function ProvisionForm() {
  const navigate = useNavigate();
  const [host, setHost] = useState("");
  const [port, setPort] = useState("22");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [agentName, setAgentName] = useState("");
  const [role, setRole] = useState("worker");
  const [isProvisioning, setIsProvisioning] = useState(false);
  const [steps, setSteps] = useState<Step[]>(initialSteps);
  const [result, setResult] = useState<ProvisionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const updateStep = (index: number, update: Partial<Step>) => {
    setSteps((prev) => prev.map((s, i) => (i === index ? { ...s, ...update } : s)));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsProvisioning(true);
    setError(null);
    setResult(null);
    setSteps(initialSteps.map((s) => ({ ...s, status: "idle" as StepStatus })));

    try {
      updateStep(0, { status: "running", message: `Connecting to ${username}@${host}:${port}...` });

      const res = await api.provision({
        host,
        port: parseInt(port),
        username,
        password,
        name: agentName || undefined,
        role,
      });

      updateStep(0, { status: "success", message: "Connected" });
      updateStep(1, { status: "success", message: "OS detected" });
      updateStep(2, { status: "success", message: "Docker ready" });
      updateStep(3, { status: "success", message: "Agent deployed" });
      updateStep(4, { status: "success", message: "Health OK" });
      updateStep(5, { status: "success", message: "Registered" });

      setResult(res);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Provisioning failed";
      setError(msg);
      updateStep(0, { status: "error", message: msg });
    } finally {
      setIsProvisioning(false);
    }
  };

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4 rounded-xl border border-gray-800 bg-gray-900 p-6">
        <h2 className="flex items-center gap-2 text-lg font-semibold">
          <Terminal className="h-5 w-5 text-brand-400" />
          Provision New Agent
        </h2>

        <div>
          <label className="mb-1 block text-sm text-gray-400">Host / IP</label>
          <div className="relative">
            <Server className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
            <input
              type="text"
              value={host}
              onChange={(e) => setHost(e.target.value)}
              placeholder="192.168.1.100"
              required
              className="w-full rounded-lg border border-gray-700 bg-gray-800 py-2 pl-10 pr-3 text-white placeholder-gray-600 focus:border-brand-500 focus:outline-none"
            />
          </div>
        </div>

        <div className="grid grid-cols-3 gap-3">
          <div>
            <label className="mb-1 block text-sm text-gray-400">Port</label>
            <input
              type="number"
              value={port}
              onChange={(e) => setPort(e.target.value)}
              className="w-full rounded-lg border border-gray-700 bg-gray-800 py-2 px-3 text-white focus:border-brand-500 focus:outline-none"
            />
          </div>
          <div className="col-span-2">
            <label className="mb-1 block text-sm text-gray-400">Agent Name</label>
            <input
              type="text"
              value={agentName}
              onChange={(e) => setAgentName(e.target.value)}
              placeholder="my-agent (auto-generated)"
              className="w-full rounded-lg border border-gray-700 bg-gray-800 py-2 px-3 text-white placeholder-gray-600 focus:border-brand-500 focus:outline-none"
            />
          </div>
        </div>

        <div>
          <label className="mb-1 block text-sm text-gray-400">SSH Username</label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="root"
              required
              className="w-full rounded-lg border border-gray-700 bg-gray-800 py-2 pl-10 pr-3 text-white placeholder-gray-600 focus:border-brand-500 focus:outline-none"
            />
          </div>
        </div>

        <div>
          <label className="mb-1 block text-sm text-gray-400">SSH Password</label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              className="w-full rounded-lg border border-gray-700 bg-gray-800 py-2 pl-10 pr-3 text-white placeholder-gray-600 focus:border-brand-500 focus:outline-none"
            />
          </div>
        </div>

        <div>
          <label className="mb-1 block text-sm text-gray-400">Role</label>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="w-full rounded-lg border border-gray-700 bg-gray-800 py-2 px-3 text-white focus:border-brand-500 focus:outline-none"
          >
            <option value="worker">Worker</option>
            <option value="supervisor">Supervisor</option>
            <option value="chat">Chat</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={isProvisioning}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-brand-600 py-2.5 font-medium text-white transition-colors hover:bg-brand-500 disabled:opacity-50"
        >
          {isProvisioning ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Provisioning...
            </>
          ) : (
            <>
              <Terminal className="h-4 w-4" />
              Deploy Agent
            </>
          )}
        </button>
      </form>

      {/* Status panel */}
      <div className="rounded-xl border border-gray-800 bg-gray-900 p-6">
        <h3 className="mb-4 text-sm font-semibold text-gray-400 uppercase tracking-wider">
          Deployment Status
        </h3>

        <div className="space-y-3">
          {steps.map((step, i) => (
            <div key={i} className="flex items-start gap-3">
              <div
                className={`mt-0.5 h-2.5 w-2.5 shrink-0 rounded-full ${
                  step.status === "idle"
                    ? "bg-gray-700"
                    : step.status === "running"
                    ? "bg-yellow-400 animate-pulse"
                    : step.status === "success"
                    ? "bg-green-400"
                    : "bg-red-400"
                }`}
              />
              <div className="min-w-0 flex-1">
                <p className="text-sm font-medium text-gray-300">{step.label}</p>
                {step.message && (
                  <p className="truncate text-xs text-gray-500">{step.message}</p>
                )}
              </div>
            </div>
          ))}
        </div>

        {error && (
          <div className="mt-4 rounded-lg bg-red-900/30 border border-red-800 p-3">
            <p className="text-sm text-red-400">{error}</p>
          </div>
        )}

        {result && (
          <div className="mt-4 space-y-2 rounded-lg bg-green-900/30 border border-green-800 p-3">
            <p className="text-sm font-medium text-green-400">✅ {result.message}</p>
            <p className="text-xs text-gray-500">Deployment ID: {result.deployment_id}</p>
            <button
              onClick={() => result.agent_id && navigate(`/agents/${result.agent_id}`)}
              className="text-sm text-brand-400 hover:underline"
            >
              View agent detail →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
