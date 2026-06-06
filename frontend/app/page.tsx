import ChatInterface from '../components/ChatInterface';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-4xl text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Customer Support</h1>
        <p className="text-gray-600">How can we help you today?</p>
      </div>
      
      <div className="w-full">
        <ChatInterface />
      </div>
    </main>
  );
}
