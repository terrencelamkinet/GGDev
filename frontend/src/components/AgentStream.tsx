import { useEffect, useRef, useState } from "react";
import type { Event } from "@/lib/api";
import { createEventStream } from "@/lib/api";

export function AgentStream() {
  const [events, setEvents] = useState<Event[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const cleanup = createEventStream((event) => {
      setEvents((prev) => [event, ...prev].slice(0, 100));
    });
    return cleanup;
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [events]);

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900">
      <div className="border-b border-gray-800 px-4 py-3">
        <h2 className="text-sm font-semibold text-gray-300">Live Event Stream</h2>
      </div>
      <div className="h-80 space-y-1 overflow-y-auto p-4 font-mono text-xs">
        {events.length === 0 && (
          <p className="text-gray-600">Waiting for events...</p>
        )}
        {events.map((evt, i) => (
          <div key={evt.id || i} className="flex gap-2 text-gray-400">
            <span className="shrink-0 text-gray-600">
              {new Date(evt.created_at).toLocaleTimeString()}
            </span>
            <span className="shrink-0 text-brand-400">{evt.type}</span>
            <span className="truncate text-gray-500">[{evt.source}]</span>
            {evt.payload && (
              <span className="truncate text-gray-600">
                {JSON.stringify(evt.payload).slice(0, 80)}
              </span>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
