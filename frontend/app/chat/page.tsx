'use client';

import { Navbar } from '@/components/navbar';
import { ChatSidebar } from '@/components/chat-sidebar';
import { ChatWindow } from '@/components/chat-window';
import { ChatInput } from '@/components/chat-input';
import { useState, useEffect, useCallback } from 'react';
import { streamChatMessages, apiRequest, API_ENDPOINTS } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/context/auth-context';
import { ProtectedRoute } from '@/components/protected-route';

interface Message {
  id?: number;
  role: 'user' | 'assistant';
  content: string;
}

interface ChatSession {
  id: number;
  title: string;
  created_at: string;
}

const initialMessages: Message[] = [
  {
    role: 'assistant',
    content: "Hello! I'm your AI medical assistant. I'm here to help you understand your health reports and answer any questions about your health in simple, easy-to-understand language. How can I help you today?",
  },
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<number | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const [isSessionsLoading, setIsSessionsLoading] = useState(false);
  const { toast } = useToast();
  const { user } = useAuth();

  const fetchSessions = useCallback(async () => {
    if (!user) return;
    try {
      setIsSessionsLoading(true);
      const data = await apiRequest<{ sessions: ChatSession[] }>(API_ENDPOINTS.CHAT.SESSIONS);
      setSessions(data.sessions);
    } catch (error) {
      console.error('Fetch sessions error:', error);
    } finally {
      setIsSessionsLoading(false);
    }
  }, [user]);

  const fetchHistory = useCallback(async (sessionId: number) => {
    try {
      setIsLoading(true);
      const data = await apiRequest<{ messages: Message[] }>(`${API_ENDPOINTS.CHAT.HISTORY}?session_id=${sessionId}`);
      setMessages(data.messages.length > 0 ? data.messages : initialMessages);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch chat history.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    if (user) {
      fetchSessions();
    }
  }, [user, fetchSessions]);

  const handleNewChat = () => {
    setMessages(initialMessages);
    setActiveSessionId(undefined);
  };

  const handleSessionSelect = (id: number) => {
    setActiveSessionId(id);
    fetchHistory(id);
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    const userMessage: Message = { role: 'user', content };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      let assistantContent = '';
      setMessages((prev) => [...prev, { role: 'assistant', content: '' }]);

      for await (const chunk of streamChatMessages(content, activeSessionId)) {
        if (chunk.content) {
          assistantContent += chunk.content;
          setMessages((prev) => {
            const newMessages = [...prev];
            if (newMessages.length > 0) {
              const lastMsg = newMessages[newMessages.length - 1];
              if (lastMsg.role === 'assistant') {
                newMessages[newMessages.length - 1] = {
                  role: 'assistant',
                  content: assistantContent,
                };
              }
            }
            return newMessages;
          });
        }
        
        if (chunk.session_id && !activeSessionId) {
          setActiveSessionId(chunk.session_id);
          fetchSessions();
        }
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to connect to the medical assistant. Please check your connection.',
        variant: 'destructive',
      });
      console.error('Chat error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="flex h-screen flex-col bg-background">
        <Navbar />
        <div className="flex flex-1 overflow-hidden">
          <ChatSidebar 
            sessions={sessions} 
            activeSessionId={activeSessionId}
            onSessionSelect={handleSessionSelect}
            onNewChat={handleNewChat}
            isLoading={isSessionsLoading}
          />
          <div className="flex flex-1 flex-col">
            <ChatWindow messages={messages} isLoading={isLoading} />
            <ChatInput onSend={handleSendMessage} />
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
