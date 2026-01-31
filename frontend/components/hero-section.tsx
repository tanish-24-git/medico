'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Upload, MessageSquare, ArrowRight, AlertCircle, LogIn, UserPlus } from 'lucide-react';
import { useAuth } from '@/context/auth-context';
import { useSearchParams } from 'next/navigation';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

export function HeroSection() {
  const { user, signInWithGoogle } = useAuth();
  const searchParams = useSearchParams();
  const isRedirected = searchParams.get('redirect');

  return (
    <section className="relative overflow-hidden border-b border-border bg-background py-20 sm:py-32">
      <div className="absolute inset-0 -z-10">
        <div className="absolute right-0 top-0 h-96 w-96 rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute left-1/4 top-1/3 h-80 w-80 rounded-full bg-secondary/5 blur-3xl" />
      </div>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        
        {isRedirected && !user && (
          <div className="mb-8 animate-in fade-in slide-in-from-top-4 duration-500">
            <Alert variant="destructive" className="border-primary/50 bg-primary/5">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Authentication Required</AlertTitle>
              <AlertDescription>
                Please sign in to access the {isRedirected.replace('/', '')} page.
              </AlertDescription>
            </Alert>
          </div>
        )}

        <div className="grid gap-12 lg:grid-cols-2 lg:gap-8">
          <div className="flex flex-col justify-center">
            <h1 className="animate-fade-in-up text-4xl font-bold tracking-tight text-foreground sm:text-5xl md:text-6xl">
              MedicoChatbot
            </h1>
            <p className="animate-fade-in-up mt-2 text-2xl font-semibold text-primary [animation-delay:100ms]">
              Understand Your Health Reports in Simple Words.
            </p>
            <p className="animate-fade-in-up mt-6 text-lg text-foreground/70 [animation-delay:200ms]">
              Upload blood reports, ask questions, and chat with an AI medical assistant that explains everything clearly.
            </p>

            <div className="animate-fade-in-up mt-10 flex flex-col gap-4 sm:flex-row [animation-delay:300ms]">
              {user ? (
                <>
                  <Link href="/chat">
                    <Button size="lg" className="w-full gap-2 bg-primary text-primary-foreground hover:bg-primary/90 sm:w-auto">
                      <MessageSquare className="h-5 w-5" />
                      Go to Chat
                    </Button>
                  </Link>
                  <Link href="/reports">
                    <Button size="lg" variant="outline" className="w-full gap-2 sm:w-auto bg-transparent">
                      <Upload className="h-5 w-5" />
                      View Reports
                    </Button>
                  </Link>
                </>
              ) : (
                <>
                  <Button 
                    size="lg" 
                    onClick={() => signInWithGoogle()}
                    className="w-full gap-2 bg-primary text-primary-foreground hover:bg-primary/90 sm:w-auto"
                  >
                    <UserPlus className="h-5 w-5" />
                    Sign Up Now
                  </Button>
                  <Button 
                    size="lg" 
                    variant="outline" 
                    onClick={() => signInWithGoogle()}
                    className="w-full gap-2 sm:w-auto bg-transparent"
                  >
                    <LogIn className="h-5 w-5" />
                    Login
                  </Button>
                </>
              )}
            </div>
          </div>

          <div className="flex items-center justify-center">
            <div className="relative w-full">
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/10 to-secondary/10 blur-2xl" />
              <div className="relative rounded-2xl border border-border bg-card p-6 shadow-lg">
                <div className="space-y-4">
                  <div className="flex gap-3">
                    <div className="h-8 w-8 rounded-full bg-primary/20" />
                    <div className="flex-1">
                      <div className="h-2 w-24 rounded bg-muted" />
                      <div className="mt-2 h-2 w-32 rounded bg-muted" />
                    </div>
                  </div>
                  <div className="flex justify-end gap-3">
                    <div className="flex-1">
                      <div className="h-2 w-24 rounded bg-primary/30" />
                      <div className="mt-2 h-2 w-32 rounded bg-primary/30" />
                    </div>
                    <div className="h-8 w-8 rounded-full bg-primary/30" />
                  </div>
                  <div className="flex gap-3">
                    <div className="h-8 w-8 rounded-full bg-primary/20" />
                    <div className="flex-1">
                      <div className="h-2 w-32 rounded bg-muted" />
                      <div className="mt-2 h-2 w-28 rounded bg-muted" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
