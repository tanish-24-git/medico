'use client';

import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
}

export function ChatMessage({ role, content }: ChatMessageProps) {
  return (
    <div className={`animate-fade-in-up flex gap-4 ${role === 'user' ? 'flex-row-reverse' : ''}`}>
      <div
        className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
          role === 'user' ? 'bg-primary' : 'bg-secondary'
        }`}
      >
        {role === 'user' ? (
          <User className="h-5 w-5 text-primary-foreground" />
        ) : (
          <Bot className="h-5 w-5 text-foreground" />
        )}
      </div>
      <div className={`flex max-w-2xl gap-4 ${role === 'user' ? 'flex-row-reverse' : ''}`}>
        <div
          className={`rounded-lg px-4 py-3 ${
            role === 'user'
              ? 'bg-primary text-primary-foreground'
              : 'bg-muted text-foreground'
          }`}
        >
          <p className="text-sm leading-relaxed">{content}</p>
        </div>
      </div>
    </div>
  );
}
