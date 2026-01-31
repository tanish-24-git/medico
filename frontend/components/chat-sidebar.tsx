'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Plus, MessageSquare, Home } from 'lucide-react';

const previousChats = [
  'Blood pressure concerns',
  'Cholesterol levels',
  'Sugar test results',
  'Recent blood work',
];

export function ChatSidebar() {
  return (
    <div className="hidden h-screen flex-col border-r border-border bg-card/50 lg:flex lg:w-64">
      <div className="border-b border-border p-4">
        <Link href="/" className="flex items-center gap-2 transition-colors hover:text-primary">
          <Home className="h-4 w-4" />
          <span className="text-sm font-medium">Back Home</span>
        </Link>
      </div>

      <div className="p-4">
        <Button size="sm" className="w-full gap-2 bg-primary text-primary-foreground hover:bg-primary/90">
          <Plus className="h-4 w-4" />
          New Chat
        </Button>
      </div>

      <ScrollArea className="flex-1">
        <div className="space-y-2 p-4">
          <p className="text-xs font-semibold uppercase text-foreground/50">Previous Chats</p>
          {previousChats.map((chat, index) => (
            <button
              key={index}
              className="w-full truncate rounded-lg px-3 py-2 text-left text-sm text-foreground/70 transition-colors hover:bg-background/50 hover:text-foreground"
            >
              {chat}
            </button>
          ))}
        </div>
      </ScrollArea>

      <div className="border-t border-border p-4 text-xs text-foreground/50">
        <p>© 2024 MedicoChatbot</p>
        <p>Secure & Private</p>
      </div>
    </div>
  );
}
