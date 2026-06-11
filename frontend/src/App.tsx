import { Routes, Route } from "react-router-dom";
import { NavBar } from "./components/NavBar";
import Dashboard from "./pages/Dashboard";
import Agents from "./pages/Agents";
import Provision from "./pages/Provision";
import AgentDetail from "./pages/AgentDetail";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <NavBar />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/agents" element={<Agents />} />
          <Route path="/agents/:id" element={<AgentDetail />} />
          <Route path="/provision" element={<Provision />} />
        </Routes>
      </main>
    </div>
  );
}
