'use client';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Paperclip } from 'lucide-react';
import { useState } from 'react';

interface ChatInputProps {
  onSend?: (message: string) => void;
}

export function ChatInput({ onSend }: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim()) {
      onSend?.(message);
      setMessage('');
    }
  };

  return (
    <div className="border-t border-border bg-background p-4">
      <div className="mx-auto max-w-4xl">
        <div className="flex gap-3">
          <Button size="icon" variant="outline" className="shrink-0 bg-transparent">
            <Paperclip className="h-5 w-5" />
          </Button>
          <Input
            placeholder="Ask about your health report..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            className="flex-1"
          />
          <Button
            size="icon"
            className="shrink-0 bg-primary text-primary-foreground hover:bg-primary/90"
            onClick={handleSend}
          >
            <Send className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </div>
  );
}
