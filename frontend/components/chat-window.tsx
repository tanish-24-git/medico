import { ScrollArea } from '@/components/ui/scroll-area';
import { ChatMessage } from '@/components/chat-message';
import { useEffect, useRef } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatWindowProps {
  messages: Message[];
  isLoading?: boolean;
}

export function ChatWindow({ messages, isLoading }: ChatWindowProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className="flex flex-1 flex-col overflow-hidden">
      <ScrollArea className="flex-1">
        <div className="space-y-6 p-6">
          {messages.map((message, index) => (
            <ChatMessage key={index} role={message.role} content={message.content} />
          ))}
          {isLoading && (!messages.length || messages[messages.length - 1].role !== 'assistant' || !messages[messages.length - 1].content) && (
            <div className="flex justify-start">
              <div className="rounded-lg bg-muted px-4 py-2 text-sm animate-pulse">
                Assistant is thinking...
              </div>
            </div>
          )}
          <div ref={scrollRef} />
        </div>
      </ScrollArea>
    </div>
  );
}
