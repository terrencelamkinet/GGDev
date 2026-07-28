const BASE = '';

async function get<T>(url: string): Promise<T> {
  const res = await fetch(`${BASE}${url}`);
  if (!res.ok) {
    const body = await res.text();
    let detail: string;
    try {
      const j = JSON.parse(body);
      detail = j.detail || j.message || body;
    } catch {
      detail = body;
    }
    throw { detail, status: res.status };
  }
  return res.json();
}

async function post<T>(url: string, data: any): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const body = await res.text();
    let detail: string;
    try {
      const j = JSON.parse(body);
      detail = j.detail || j.message || body;
    } catch {
      detail = body;
    }
    throw { detail, status: res.status };
  }
  return res.json();
}

async function put<T>(url: string, data: any): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const body = await res.text();
    let detail: string;
    try {
      const j = JSON.parse(body);
      detail = j.detail || j.message || body;
    } catch {
      detail = body;
    }
    throw { detail, status: res.status };
  }
  return res.json();
}

async function del<T>(url: string): Promise<T> {
  const res = await fetch(`${BASE}${url}`, { method: 'DELETE' });
  if (!res.ok) {
    const body = await res.text();
    let detail: string;
    try {
      const j = JSON.parse(body);
      detail = j.detail || j.message || body;
    } catch {
      detail = body;
    }
    throw { detail, status: res.status };
  }
  return res.json();
}

export const apiClient = { get, post, put, del };
