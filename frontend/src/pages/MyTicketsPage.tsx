import React, { useState, useEffect, useMemo } from 'react';
import type { TicketResponse, TicketStatus } from '../types/ticket';
import { ticketService } from '../services/ticketService';
import TicketList from '../components/tickets/TicketList';
import TicketFilters from '../components/tickets/TicketFilters';
import TicketDetailsModal from '../components/tickets/TicketDetailsModal';

const MyTicketsPage: React.FC = () => {
  const [tickets, setTickets] = useState<TicketResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<TicketStatus | 'all'>('all');
  const [selectedTicket, setSelectedTicket] = useState<TicketResponse | null>(null);

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const data = await ticketService.getMyTickets();
        setTickets(data);
      } catch (error) {
        console.error('Failed to fetch tickets:', error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchTickets();
  }, []);

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
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">My Tickets</h1>
          <p className="text-sm text-gray-500 mt-1">View and manage your support requests.</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <TicketFilters 
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          statusFilter={statusFilter}
          onStatusFilterChange={setStatusFilter}
        />

        <TicketList 
          tickets={filteredTickets} 
          isLoading={isLoading} 
          onTicketClick={setSelectedTicket}
          emptyMessage={searchQuery || statusFilter !== 'all' ? "No matching tickets found" : "You haven't created any tickets yet"}
          emptySubMessage={searchQuery || statusFilter !== 'all' ? "Try adjusting your search or filters to find what you're looking for." : "When you need help, your tickets will appear here."}
        />
      </div>

      {selectedTicket && (
        <TicketDetailsModal 
          ticket={selectedTicket} 
          isOpen={!!selectedTicket} 
          onClose={() => setSelectedTicket(null)} 
        />
      )}
    </div>
  );
};

export default MyTicketsPage;
