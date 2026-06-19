import React from 'react';
import { Bot, Shield, CreditCard, Ticket } from 'lucide-react';

interface AgentBadgeProps {
  agentName: string;
}

const AgentBadge: React.FC<AgentBadgeProps> = ({ agentName }) => {
  const getAgentDetails = () => {
    switch (agentName.toLowerCase()) {
      case 'billing':
      case 'billing agent':
        return { icon: <CreditCard className="w-3 h-3" />, color: 'bg-green-100 text-green-700 border-green-200' };
      case 'ticket':
      case 'ticket agent':
        return { icon: <Ticket className="w-3 h-3" />, color: 'bg-purple-100 text-purple-700 border-purple-200' };
      case 'escalation':
      case 'escalation agent':
        return { icon: <Shield className="w-3 h-3" />, color: 'bg-red-100 text-red-700 border-red-200' };
      default:
        return { icon: <Bot className="w-3 h-3" />, color: 'bg-blue-100 text-blue-700 border-blue-200' };
    }
  };

  const { icon, color } = getAgentDetails();

  return (
    <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium border ${color} mb-2 shadow-sm`}>
      {icon}
      <span>{agentName.replace(/Agent/i, '').trim()} Agent</span>
    </div>
  );
};

export default AgentBadge;
