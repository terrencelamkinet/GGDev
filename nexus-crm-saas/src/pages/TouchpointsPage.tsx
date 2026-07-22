import { Phone, Users, Mail, ScanLine } from 'lucide-react';

const items = [
  { type: 'call', title: 'Call with Peter Wong', desc: 'Discussed Q4 pipeline, demo scheduled', company: 'Kinetix Systems', contact: 'Peter Wong', time: '2h ago', icon: Phone, color: 'text-blue-600 bg-blue-100' },
  { type: 'meeting', title: 'Vendor Briefing - HPE', desc: 'New Aruba networking lineup', company: 'HPE Hong Kong', contact: '—', time: '4h ago', icon: Users, color: 'text-emerald-600 bg-emerald-100' },
  { type: 'email', title: 'Proposal sent', desc: 'Fortinet Firewall renewal quote', company: 'HCL Technologies', contact: 'Mary Chen', time: '1d ago', icon: Mail, color: 'text-purple-600 bg-purple-100' },
  { type: 'namecard', title: 'NameCard scanned', desc: 'Director at Digidations', company: 'Digidations HK', contact: 'Cathy Cheung', time: '1d ago', icon: ScanLine, color: 'text-amber-600 bg-amber-100' },
  { type: 'meeting', title: 'Solution Design Workshop', desc: 'HKMA AppScan architecture review', company: 'Kinetix Systems', contact: 'Peter Wong', time: '2d ago', icon: Users, color: 'text-emerald-600 bg-emerald-100' },
];

export default function TouchpointsPage() {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Touchpoints</h1>
        <p className="text-sm text-slate-500 mt-1">Activity timeline</p>
      </div>
      <div className="panel">
        <div className="timeline">
          {items.map((item, i) => (
            <div key={i} className="tl-item">
              <div className={`list-icon ${item.color}`}>
                <item.icon />
              </div>
              <div className="list-main">
                <p className="list-title">{item.title}</p>
                <p className="list-sub">{item.desc}</p>
                <div className="list-meta">
                  <span>🏢 {item.company}</span>
                  {item.contact !== '—' && <span>👤 {item.contact}</span>}
                  <span className="meta-time">{item.time}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
