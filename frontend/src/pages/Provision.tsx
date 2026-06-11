import { ProvisionForm } from "@/components/ProvisionForm";

export default function Provision() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Provision Agent</h1>
        <p className="text-gray-500">
          Deploy a new AI agent to any server via SSH — one click, fully automated.
        </p>
      </div>
      <ProvisionForm />
    </div>
  );
}
