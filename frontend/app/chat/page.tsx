'use client';

import { Navbar } from '@/components/navbar';
import { ChatSidebar } from '@/components/chat-sidebar';
import { ChatWindow } from '@/components/chat-window';
import { ChatInput } from '@/components/chat-input';
import { useState, useEffect } from 'react';
import { streamChatMessages } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const initialMessages: Message[] = [
  {
    role: 'assistant',
    content: "Hello! I'm your AI medical assistant. I'm here to help you understand your health reports and answer any questions about your health in simple, easy-to-understand language. How can I help you today?",
  },
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    // Add user message
    const userMessage: Message = { role: 'user', content };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      let assistantContent = '';
      
      // Add placeholder for assistant message
      setMessages((prev) => [...prev, { role: 'assistant', content: '' }]);

      for await (const chunk of streamChatMessages(content)) {
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
    <div className="flex h-screen flex-col bg-background">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <ChatSidebar />
        <div className="flex flex-1 flex-col">
          <ChatWindow messages={messages} isLoading={isLoading} />
          <ChatInput onSend={handleSendMessage} />
        </div>
      </div>
    </div>
  );
}
