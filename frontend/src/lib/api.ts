/**
 * AI One API client — typed HTTP + WebSocket helpers.
 */

const API_BASE = "/api";
const WS_BASE = `${location.protocol === "https:" ? "wss:" : "ws:"}//${location.host}/ws`;

// ── Types ──────────────────────────────────────────────────────────────────

export interface Agent {
  id: string;
  name: string;
  host: string;
  port: number;
  role: string;
  status: "online" | "offline" | "provisioning" | "error";
  api_key?: string;
  config?: Record<string, unknown>;
  last_heartbeat?: string;
  created_at: string;
  updated_at: string;
}

export interface ProvisionRequest {
  host: string;
  port?: number;
  username: string;
  password: string;
  name?: string;
  role?: string;
}

export interface ProvisionResponse {
  deployment_id: string;
  agent_id?: string;
  status: string;
  message: string;
}

export interface Event {
  id: string;
  type: string;
  source: string;
  target?: string;
  payload?: Record<string, unknown>;
  created_at: string;
}

// ── HTTP Client ────────────────────────────────────────────────────────────

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API ${res.status}: ${body}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  // Agents
  listAgents: () => request<Agent[]>("/agents/"),

  getAgent: (id: string) => request<Agent>(`/agents/${id}`),

  createAgent: (data: Partial<Agent>) =>
    request<Agent>("/agents/", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  updateAgent: (id: string, data: Partial<Agent>) =>
    request<Agent>(`/agents/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  deleteAgent: (id: string) =>
    request<void>(`/agents/${id}`, { method: "DELETE" }),

  // Provision
  provision: (data: ProvisionRequest) =>
    request<ProvisionResponse>("/provision/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

// ── WebSocket ──────────────────────────────────────────────────────────────

export function createEventStream(
  onEvent: (event: Event) => void,
  onError?: (err: Event) => void
): () => void {
  const ws = new WebSocket(`${WS_BASE}/stream`);

  ws.onopen = () => {
    // Send periodic pings to keep connection alive
    const pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send("ping");
      } else {
        clearInterval(pingInterval);
      }
    }, 30_000);
  };

  ws.onmessage = (msg) => {
    try {
      const data = JSON.parse(msg.data);
      onEvent(data);
    } catch {
      // ignore non-JSON frames
    }
  };

  ws.onerror = () => {
    onError?.({
      id: "",
      type: "connection.error",
      source: "client",
      payload: { message: "WebSocket connection error" },
      created_at: new Date().toISOString(),
    });
  };

  // Return cleanup function
  return () => ws.close();
}
