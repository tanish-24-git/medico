'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Plus, MessageSquare, Home, Loader2 } from 'lucide-react';

interface ChatSession {
  id: number;
  title: string;
  created_at: string;
}

interface ChatSidebarProps {
  sessions: ChatSession[];
  activeSessionId?: number;
  onSessionSelect: (id: number) => void;
  onNewChat: () => void;
  isLoading?: boolean;
}

export function ChatSidebar({ 
  sessions, 
  activeSessionId, 
  onSessionSelect, 
  onNewChat,
  isLoading 
}: ChatSidebarProps) {
  return (
    <div className="hidden h-screen flex-col border-r border-border bg-card/50 lg:flex lg:w-64">
      <div className="border-b border-border p-4">
        <Link href="/" className="flex items-center gap-2 transition-colors hover:text-primary text-foreground">
          <Home className="h-4 w-4" />
          <span className="text-sm font-medium">Back Home</span>
        </Link>
      </div>

      <div className="p-4">
        <Button 
          size="sm" 
          className="w-full gap-2 bg-primary text-primary-foreground hover:bg-primary/90"
          onClick={onNewChat}
        >
          <Plus className="h-4 w-4" />
          New Chat
        </Button>
      </div>

      <ScrollArea className="flex-1">
        <div className="space-y-2 p-4">
          <p className="text-xs font-semibold uppercase text-foreground/50">Previous Chats</p>
          {isLoading ? (
            <div className="flex py-4 justify-center">
              <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
            </div>
          ) : sessions.length > 0 ? (
            sessions.map((chat) => (
              <button
                key={chat.id}
                onClick={() => onSessionSelect(chat.id)}
                className={`w-full truncate rounded-lg px-3 py-2 text-left text-sm transition-colors hover:bg-background/50 flex items-center gap-2 ${
                  activeSessionId === chat.id ? 'bg-background text-primary font-medium' : 'text-foreground/70 hover:text-foreground'
                }`}
              >
                <MessageSquare className="h-3 w-3 shrink-0" />
                <span className="truncate">{chat.title || 'Untitled Chat'}</span>
              </button>
            ))
          ) : (
            <p className="py-4 text-xs text-center text-muted-foreground italic">No previous chats</p>
          )}
        </div>
      </ScrollArea>

      <div className="border-t border-border p-4 text-xs text-foreground/50">
        <p>© 2024 MedicoChatbot</p>
        <p>Secure & Private</p>
      </div>
    </div>
  );
}
