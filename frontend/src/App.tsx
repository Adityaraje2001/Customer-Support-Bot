import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import AdminRoute from './components/AdminRoute';
import AppLayout from './components/layout/AppLayout';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ChatPage from './pages/ChatPage';
import MyTicketsPage from './pages/MyTicketsPage';
import ProfilePage from './pages/ProfilePage';
import ConversationHistoryPage from './pages/ConversationHistoryPage';
import AdminTicketsPage from './pages/AdminTicketsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import KnowledgeBasePage from './pages/KnowledgeBasePage';
import FeedbackPage from './pages/FeedbackPage';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <Toaster position="top-right" />
      <Routes>
        {/* Public Routes with old Navbar */}
        <Route path="/login" element={<><Navbar /><LoginPage /></>} />
        <Route path="/register" element={<><Navbar /><RegisterPage /></>} />
        
        {/* Protected Routes with AppLayout */}
        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/my-tickets" element={<MyTicketsPage />} />
            <Route path="/conversations" element={<ConversationHistoryPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            
            {/* Admin Only Routes */}
            <Route element={<AdminRoute />}>
              <Route path="/admin/tickets" element={<AdminTicketsPage />} />
              <Route path="/admin/analytics" element={<AnalyticsPage />} />
              <Route path="/admin/knowledge-base" element={<KnowledgeBasePage />} />
              <Route path="/admin/feedback" element={<FeedbackPage />} />
            </Route>
          </Route>
        </Route>
        
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </div>
  );
};

export default App;
