import React, { useState, useEffect, useMemo } from 'react';
import toast from 'react-hot-toast';
import type { TicketResponse, TicketStatus } from '../types/ticket';
import { ticketService } from '../services/ticketService';
import TicketFilters from '../components/tickets/TicketFilters';
import TicketStatusBadge from '../components/tickets/TicketStatusBadge';
import AdminTicketActions from '../components/tickets/AdminTicketActions';
import TicketEmptyState from '../components/tickets/TicketEmptyState';

const AdminTicketsPage: React.FC = () => {
  const [tickets, setTickets] = useState<TicketResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<TicketStatus | 'all'>('all');

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const data = await ticketService.getAllTickets();
        setTickets(data);
      } catch (error) {
        console.error('Failed to fetch tickets:', error);
        toast.error('Failed to load tickets');
      } finally {
        setIsLoading(false);
      }
    };
    fetchTickets();
  }, []);

  const handleTicketUpdate = (updatedTicket: TicketResponse) => {
    setTickets(prev => prev.map(t => t.id === updatedTicket.id ? updatedTicket : t));
    toast.success(`Ticket #${updatedTicket.id} updated`);
  };

  const filteredTickets = useMemo(() => {
    return tickets.filter((ticket) => {
      const matchesSearch = 
        ticket.id.toString().includes(searchQuery.toLowerCase()) || 
        ticket.question.toLowerCase().includes(searchQuery.toLowerCase());
        
      const matchesStatus = 
        statusFilter === 'all' || 
        ticket.status.toLowerCase() === statusFilter.toLowerCase();
        
      return matchesSearch && matchesStatus;
    });
  }, [tickets, searchQuery, statusFilter]);

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Ticket Management</h1>
          <p className="text-sm text-gray-500 mt-1">Manage all customer support tickets across the platform.</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <TicketFilters 
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          statusFilter={statusFilter}
          onStatusFilterChange={setStatusFilter}
        />

        {isLoading ? (
          <div className="animate-pulse space-y-4">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="h-16 bg-gray-100 rounded-lg w-full"></div>
            ))}
          </div>
        ) : filteredTickets.length === 0 ? (
          <TicketEmptyState 
            message="No tickets found" 
            subMessage="Try adjusting your search or filter to find tickets." 
          />
        ) : (
          <div className="overflow-x-auto rounded-lg border border-gray-200">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ID
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Issue
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created Date
                  </th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredTickets.map((ticket) => (
                  <tr key={ticket.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      #{ticket.id}
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900 line-clamp-1 max-w-md" title={ticket.question}>
                        {ticket.question}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <TicketStatusBadge status={ticket.status} />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {ticket.created_at ? new Date(ticket.created_at).toLocaleDateString() : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex justify-end">
                        <AdminTicketActions ticket={ticket} onUpdate={handleTicketUpdate} />
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminTicketsPage;
