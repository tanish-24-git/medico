'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Heart } from 'lucide-react';

export function Navbar() {
  return (
    <nav className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <Heart className="h-5 w-5 text-primary-foreground" />
          </div>
          <span className="text-lg font-semibold text-foreground">MedicoChatbot</span>
        </div>

        <div className="hidden gap-8 md:flex">
          <Link href="/" className="text-sm font-medium text-foreground/70 transition-colors hover:text-foreground">
            Home
          </Link>
          <Link href="/chat" className="text-sm font-medium text-foreground/70 transition-colors hover:text-foreground">
            Chat
          </Link>
          <Link href="/reports" className="text-sm font-medium text-foreground/70 transition-colors hover:text-foreground">
            Reports
          </Link>
          <Link href="/about" className="text-sm font-medium text-foreground/70 transition-colors hover:text-foreground">
            About
          </Link>
        </div>

        <Button className="bg-primary text-primary-foreground hover:bg-primary/90">Sign In</Button>
      </div>
    </nav>
  );
}
