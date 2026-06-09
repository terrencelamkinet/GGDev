import { Link, useLocation } from "react-router-dom";
import { Cpu, Server, Plus, LayoutDashboard } from "lucide-react";

const navItems = [
  { path: "/", label: "Dashboard", icon: LayoutDashboard },
  { path: "/agents", label: "Agents", icon: Cpu },
  { path: "/provision", label: "Provision", icon: Plus },
];

export function NavBar() {
  const location = useLocation();

  return (
    <nav className="border-b border-gray-800 bg-gray-900/80 backdrop-blur-sm">
      <div className="container mx-auto flex items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2 text-xl font-bold text-white">
          <Server className="h-6 w-6 text-brand-500" />
          <span>AI One</span>
        </Link>

        <div className="flex items-center gap-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-brand-600 text-white"
                    : "text-gray-400 hover:bg-gray-800 hover:text-white"
                }`}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
