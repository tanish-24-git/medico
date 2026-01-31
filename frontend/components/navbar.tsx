'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Heart, LogOut, User } from 'lucide-react';
import { useAuth } from '@/context/auth-context';
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger 
} from '@/components/ui/dropdown-menu';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

export function Navbar() {
  const { user, signInWithGoogle, logout } = useAuth();

  return (
    <nav className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <Heart className="h-5 w-5 text-primary-foreground" />
          </div>
          <span className="text-lg font-semibold text-foreground">MedicoChatbot</span>
        </Link>

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

        <div className="flex items-center gap-3">
          {!user ? (
            <>
              <Button 
                variant="ghost"
                onClick={() => signInWithGoogle()} 
                className="text-foreground/70 hover:text-foreground"
              >
                Login
              </Button>
              <Button 
                onClick={() => signInWithGoogle()} 
                className="bg-primary text-primary-foreground hover:bg-primary/90"
              >
                Sign Up
              </Button>
            </>
          ) : (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-9 w-9 rounded-full">
                  <Avatar className="h-9 w-9">
                    <AvatarImage src={user.photoURL || ''} alt={user.displayName || ''} />
                    <AvatarFallback>{user.displayName?.charAt(0) || 'U'}</AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuItem className="flex flex-col items-start gap-1">
                  <span className="text-sm font-medium">{user.displayName}</span>
                  <span className="text-xs text-muted-foreground">{user.email}</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => logout()} className="text-destructive focus:text-destructive">
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Log out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      </div>
    </nav>
  );
}
