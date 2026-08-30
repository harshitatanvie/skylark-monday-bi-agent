import React, { useState, useEffect } from 'react';
import { Header } from './components/Layout/Header';
import { Sidebar } from './components/Layout/Sidebar';
import { ChatFeed } from './components/Chat/ChatFeed';
import { DataQualityDrawer } from './components/Dashboard/DataQualityDrawer';
import { LeadershipModal } from './components/Leadership/LeadershipModal';
import { ConfigModal } from './components/Layout/ConfigModal';
import { ChatMessage, DataQualityReport, MondayStatusData } from './types';
import { sendChatMessage, fetchMondayStatus, fetchDataQuality } from './services/api';

export const App: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isDemoMode, setIsDemoMode] = useState(true);
  
  const [mondayStatus, setMondayStatus] = useState<MondayStatusData | null>(null);
  const [dataQualityReport, setDataQualityReport] = useState<DataQualityReport | null>(null);
  
  const [isDataQualityDrawerOpen, setIsDataQualityDrawerOpen] = useState(false);
  const [isLeadershipModalOpen, setIsLeadershipModalOpen] = useState(false);
  const [isConfigModalOpen, setIsConfigModalOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Initial load status & data quality check
  useEffect(() => {
    fetchMondayStatus()
      .then((status) => {
        setMondayStatus(status);
        setIsDemoMode(status.is_demo_mode);
      })
      .catch((err) => console.error('Failed to fetch Monday status:', err));

    fetchDataQuality(isDemoMode)
      .then((report) => setDataQualityReport(report))
      .catch((err) => console.error('Failed to fetch Data Quality:', err));
  }, [isDemoMode]);

  const handleSendMessage = async (promptText: string) => {
    const userMsgId = Date.now().toString();
    const userMsg: ChatMessage = {
      id: userMsgId,
      sender: 'user',
      text: promptText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const responseData = await sendChatMessage(promptText, isDemoMode);
      
      const aiMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: responseData.answer_markdown,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        response_data: responseData,
      };

      setMessages((prev) => [...prev, aiMsg]);
      if (responseData.data_quality_report) {
        setDataQualityReport(responseData.data_quality_report);
      }
    } catch (err: any) {
      console.error('Error sending chat message:', err);
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: `### ⚠️ Connection Error\n\nUnable to process query at this time. ${
          err.response?.data?.detail || err.message || 'Please verify backend service is running.'
        }`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-slate-950 text-slate-100 font-sans">
      <Header
        mondayStatus={mondayStatus}
        dataQualityReport={dataQualityReport}
        onOpenLeadershipModal={() => setIsLeadershipModalOpen(true)}
        onOpenDataQualityDrawer={() => setIsDataQualityDrawerOpen(true)}
        onOpenConfigModal={() => setIsConfigModalOpen(true)}
      />

      <div className="flex-1 flex overflow-hidden relative">
        <Sidebar
          onSelectPrompt={handleSendMessage}
          onOpenLeadershipModal={() => setIsLeadershipModalOpen(true)}
          onOpenDataQualityDrawer={() => setIsDataQualityDrawerOpen(true)}
          isOpen={isSidebarOpen}
          onCloseMobile={() => setIsSidebarOpen(false)}
        />

        <main className="flex-1 flex flex-col h-full overflow-hidden">
          <ChatFeed
            messages={messages}
            isLoading={isLoading}
            onSendMessage={handleSendMessage}
            onClearChat={handleClearChat}
            onOpenDataQualityDrawer={() => setIsDataQualityDrawerOpen(true)}
          />
        </main>
      </div>

      <DataQualityDrawer
        isOpen={isDataQualityDrawerOpen}
        onClose={() => setIsDataQualityDrawerOpen(false)}
        report={dataQualityReport}
      />

      <LeadershipModal
        isOpen={isLeadershipModalOpen}
        onClose={() => setIsLeadershipModalOpen(false)}
        isDemoMode={isDemoMode}
      />

      <ConfigModal
        isOpen={isConfigModalOpen}
        onClose={() => setIsConfigModalOpen(false)}
        status={mondayStatus}
        isDemoMode={isDemoMode}
        onToggleDemoMode={(val) => setIsDemoMode(val)}
      />
    </div>
  );
};

export default App;
