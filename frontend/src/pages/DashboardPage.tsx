import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { ticketService } from '../services/ticketService';
import type { TicketResponse } from '../types/ticket';
import { MessageSquare, Ticket, CheckCircle2, Shield, Loader2 } from 'lucide-react';

const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const [openTickets, setOpenTickets] = useState<TicketResponse[]>([]);
  const [resolvedTickets, setResolvedTickets] = useState<TicketResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (user?.role === 'admin') {
      const fetchTickets = async () => {
        setIsLoading(true);
        try {
          const [open, resolved] = await Promise.all([
            ticketService.getOpenTickets(),
            ticketService.getResolvedTickets()
          ]);
          setOpenTickets(open);
          setResolvedTickets(resolved);
        } catch (error) {
          console.error("Failed to fetch tickets:", error);
        } finally {
          setIsLoading(false);
        }
      };
      
      fetchTickets();
    }
  }, [user]);

  // Mock value for conversations
  const totalConversations = 124;

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Welcome back, {user?.username}. Here's what's happening today.
          </p>
        </div>
      </div>

      {/* Dashboard Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {/* Card 1: Total Conversations */}
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-200 p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-blue-50 rounded-md p-3">
              <MessageSquare className="h-6 w-6 text-blue-600" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Total Conversations</dt>
                <dd className="text-2xl font-semibold text-gray-900">{totalConversations}</dd>
              </dl>
            </div>
          </div>
        </div>

        {/* Card 2: Open Tickets */}
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-200 p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-amber-50 rounded-md p-3">
              <Ticket className="h-6 w-6 text-amber-600" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Open Tickets</dt>
                <dd className="text-2xl font-semibold text-gray-900">
                  {user?.role === 'admin' ? (isLoading ? '...' : openTickets.length) : '4'}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        {/* Card 3: Resolved Tickets */}
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-200 p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-green-50 rounded-md p-3">
              <CheckCircle2 className="h-6 w-6 text-green-600" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Resolved Tickets</dt>
                <dd className="text-2xl font-semibold text-gray-900">
                  {user?.role === 'admin' ? (isLoading ? '...' : resolvedTickets.length) : '12'}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        {/* Card 4: Current Role */}
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-200 p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-purple-50 rounded-md p-3">
              <Shield className="h-6 w-6 text-purple-600" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Current Role</dt>
                <dd className="text-2xl font-semibold text-gray-900 capitalize">{user?.role || 'Guest'}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      {user?.role === 'admin' && (
        <div className="mt-8">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Active Tickets</h2>
          {isLoading ? (
            <div className="flex justify-center items-center py-12">
              <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
            </div>
          ) : (
            <div className="bg-white shadow-sm overflow-hidden sm:rounded-xl border border-gray-200">
              <ul className="divide-y divide-gray-200">
                {openTickets.length === 0 ? (
                  <li className="px-6 py-4 text-sm text-gray-500 text-center">No active tickets.</li>
                ) : (
                  openTickets.slice(0, 5).map((ticket) => (
                    <li key={ticket.id} className="px-6 py-4 hover:bg-gray-50">
                      <div className="flex items-center justify-between">
                        <div className="text-sm font-medium text-blue-600 truncate">Ticket #{ticket.id}</div>
                        <div className="ml-2 flex-shrink-0 flex">
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-amber-100 text-amber-800">
                            Open
                          </span>
                        </div>
                      </div>
                      <div className="mt-2 sm:flex sm:justify-between">
                        <div className="sm:flex">
                          <p className="flex items-center text-sm text-gray-500">
                            {ticket.question}
                          </p>
                        </div>
                      </div>
                    </li>
                  ))
                )}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
